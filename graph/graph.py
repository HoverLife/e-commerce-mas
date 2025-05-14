import json
from typing import Any, Dict, List, TypedDict

from typing_extensions import Annotated

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START
from langgraph.graph import add_messages
from tools.db_tools import FetchProductsTool
from tools.tools import (
    marketplace_agent_tool,
    buyer_agent_tool,
    cross_sell_agent_tool,
    item_agent_tool,
    price_negotiation_agent_tool,
)
from utils.gigachat import GigaChatClient

# 1) Все ваши инструменты
TOOLS = [
    FetchProductsTool(),
    marketplace_agent_tool,
    buyer_agent_tool,
    cross_sell_agent_tool,
    item_agent_tool,
    price_negotiation_agent_tool,
]

# 2) Состояние
class ChatState(TypedDict):
    messages: Annotated[List[Any], add_messages]

# graph/graph.py — только функция call_model

async def call_model(state: ChatState) -> Dict[str, List[Any]]:
    client = GigaChatClient()

    # 1) Собираем history
    history: List[Dict[str, Any]] = []
    for m in state["messages"]:
        history.append({"role": m.role, "content": m.content})

    # 2) Всегда на первом запросе (history длины 2) подставляем функции
    if len(state["messages"]) == 2:
        func_defs = [tool.to_openai_function() for tool in TOOLS]
        history.insert(0, {
            "role": "system",
            "content":
                "Ты — ассистент. У тебя есть функция fetch_products(category, limit). "
                "Используй её для получения списка товаров из БД.",
            "functions": func_defs
        })

    # 3) Делаем запрос
    resp = await client.chat(history)
    msg = resp["choices"][0]["message"]
    fc = msg.get("function_call")

    # 4) Если GigaChat вызвал функцию — выполняем её и второй раз зовём LLM
    if fc:
        name = fc["name"]
        try:
            args = json.loads(fc.get("arguments", "{}"))
        except json.JSONDecodeError:
            args = {}
        for tool in TOOLS:
            if tool.name == name:
                result = await tool.arun(**args)
                break
        else:
            result = {"error": f"Unknown function {name}"}

        # кладём вызов в историю
        history.append({"role": "assistant", "content": msg.get("content", "")})
        history.append({
            "role": "tool", 
            "name": name, 
            "content": json.dumps(result, ensure_ascii=False)
        })

        final = await client.chat(history)
        final_msg = final["choices"][0]["message"]
        return {"messages": [AIMessage(final_msg.get("content", ""))]}

    # 5) Иначе — обычный ответ без ошибок
    return {"messages": [AIMessage(msg.get("content", ""))]}

# 4) Сборка графа
builder = StateGraph(ChatState)
builder.add_node("model", call_model)
builder.add_edge(START, "model")
graph = builder.compile()
