import json, uuid
from langgraph.graph import StateGraph, START
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.messages import ToolMessage
from state.state import ChatState
from utils.gigachat import GigaChatClient
from tools.db_tools import TOOLS

client = GigaChatClient()

async def call_model(state: ChatState) -> dict:
    # 1) собираем history для GigaChat
    history = []
    for m in state["messages"]:
        if isinstance(m, SystemMessage):
            role = "system"
        elif isinstance(m, HumanMessage):
            role = "user"
        elif isinstance(m, AIMessage):
            role = "assistant"
        else:
            role = "tool"
        history.append({"role": role, "content": m.content})

    # 2) описываем наши функции в prompt-system
    func_defs = [tool.to_openai_function() for tool in TOOLS]
    history.insert(0, {
        "role": "system",
        "content": (
            "Ты — ассистент. У тебя есть функция fetch_products(category, limit). "
            "Когда нужно достать реальные товары из базы, "
            "вызывай функцию fetch_products в формате JSON: {\"name\":\"fetch_products\",\"arguments\":{...}} "
            "Без лишнего текста."
        )
    })

    # 3) первый вызов к GigaChat
    resp = await client.chat(history)
    msg = resp["choices"][0]["message"]
    raw = msg.get("content", "")
    fc = msg.get("function_call")
    if not fc:
        return {"messages": [AIMessage(raw)]}

    # 4) парсим вызов функции
    fn_name = fc["name"]
    try:
        args = json.loads(fc.get("arguments", "{}"))
    except:
        args = {}

    # 5) выполняем local function
    for tool in TOOLS:
        if tool.name == fn_name:
            result = await tool.arun(**args)
            break
    else:
        result = []

    result_json = json.dumps(result, ensure_ascii=False)

    # 6) пушим результат как ToolMessage и повторяем LLM
    history.append({"role": "assistant", "content": raw})
    history.append({"role": "tool", "name": fn_name, "content": result_json})
    final = await client.chat(history)
    final_text = final["choices"][0]["message"]["content"]
    return {"messages": [AIMessage(final_text)]}

# сборка графа
builder = StateGraph(ChatState)
builder.add_node("model", call_model)
builder.add_edge(START, "model")
graph = builder.compile()
