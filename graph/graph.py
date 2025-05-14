# graph/graph.py

import json
from typing import List, Dict, TypedDict, Any
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from utils.gigachat import GigaChatClient
from tools.db_tools import TOOLS  # ваш список инструментов

client = GigaChatClient()

class ChatState(TypedDict):
    messages: List[Any]
    session_id: str

async def call_model(state: ChatState) -> Dict[str, List[Any]]:
    # Преобразуем в формат OpenAI
    history: List[Dict[str, Any]] = []
    for m in state["messages"]:
        history.append({"role": m.role, "content": m.content})

    # Вставляем system prompt только при первом вызове
    if len(state["messages"]) == 1:
        history.insert(0, {
            "role": "system",
            "content": (
                "Ты — ассистент. "
                "У тебя есть функция fetch_products(category, limit). "
                "Когда нужно взять товары из БД, вызывай её через function_call."
            )
        })

    # Первый вызов LLM
    resp = await client.chat(history)
    choice = resp["choices"][0]["message"]

    # Если LLM вернул function_call
    if "function_call" in choice:
        # Заворачиваем tool_calls в AIMessage
        return {
            "messages": [
                AIMessage(content=choice.get("content", ""), tool_calls=[choice["function_call"]])
            ]
        }

    # Обычный ответ без вызова функции
    return {
        "messages": [
            AIMessage(content=choice.get("content", ""))
        ]
    }


async def execute_tool(state: ChatState) -> Dict[str, List[Any]]:
    # Найдём последний AIMessage с tool_calls
    last_ai: AIMessage = next(
        m for m in reversed(state["messages"])
        if isinstance(m, AIMessage) and getattr(m, "tool_calls", None)
    )
    fn = last_ai.tool_calls[0]
    name = fn["name"]
    args = json.loads(fn.get("arguments", "{}"))

    # Выполним соответствующий инструмент
    result = None
    for tool in TOOLS:
        if tool.name == name:
            result = await tool.arun(**args)
            break

    # Возвращаем результат как ToolMessage
    return {
        "messages": [
            ToolMessage(content=json.dumps(result, ensure_ascii=False), name=name)
        ]
    }


# Собираем граф
builder = StateGraph(ChatState)

# Регистрируем узлы по строковым именам
builder.add_node("call_model", call_model)
builder.add_node("execute_tool", execute_tool)

# Два возможных пути
builder.add_edge(START, "call_model")
builder.add_conditional_edges(
    "call_model",
    # Если после call_model появилось function_call — идём в execute_tool, иначе — в END
    lambda st: "execute_tool" if any(
        isinstance(m, AIMessage) and getattr(m, "tool_calls", None)
        for m in st["messages"]
    ) else END
)
# После execute_tool всегда возвращаемся к call_model
builder.add_edge("execute_tool", "call_model")

# Компилируем граф
graph = builder.compile()
