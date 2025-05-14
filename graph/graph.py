import json
import logging
from typing import List, Dict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from agents.marketplace_agent import marketplace_agent
from utils.gigachat import GigaChatClient

# Логирование
logger = logging.getLogger("agent_actions")

giga = GigaChatClient()

class ChatState(dict):
    """Состояние чата: содержит ключи `messages` и `session_id`."""
    pass

async def call_model(state: ChatState) -> Dict[str, List[AIMessage]]:
    # Собираем историю
    messages = state.get("messages", [])
    chat_hist = []
    for m in messages:
        if isinstance(m, SystemMessage): role = "system"
        elif isinstance(m, HumanMessage): role = "user"
        elif isinstance(m, AIMessage): role = "assistant"
        else: role = "tool"
        chat_hist.append({"role": role, "content": m.content})

    # Функции для вызова
    functions = [{
        "name": "fetch_products",
        "description": "Fetch products from the database by category",
        "parameters": {
            "type": "object",
            "properties": {"category": {"type": "string"}, "limit": {"type": "integer", "default": 0}},
            "required": ["category"]
        }
    }]
    # Добавляем системную инструкцию
    chat_hist.insert(0, {"role": "system", "content": (
        "Ты — ассистент. При необходимости вызывай функцию fetch_products(category, limit)."
    )})

    # Первый запрос
    resp = await giga.chat(chat_hist, functions=functions)
    msg = resp["choices"][0]["message"]
    content = msg.get("content", "")
    fc = msg.get("function_call")
    if not fc:
        return {"messages": [AIMessage(content)]}

    # Обработка function_call
    name = fc["name"]
    args = json.loads(fc.get("arguments", "{}"))
    if name == "fetch_products":
        items = await marketplace_agent([args.get("category")], args.get("limit", 0))
    else:
        items = []
    tools_content = json.dumps(items, ensure_ascii=False)

    # Второй запрос с результатом функции
    chat_hist.append({"role": "assistant", "content": content})
    chat_hist.append({"role": "tool", "name": name, "content": tools_content})
    final = await giga.chat(chat_hist)
    final_text = final["choices"][0]["message"]["content"]
    return {"messages": [AIMessage(final_text)], "session_id": state.get("session_id")}

# Сборка графа
builder = StateGraph(ChatState)
builder.add_node("model", call_model)
builder.add_edge(START, "model")

graph = builder.compile()