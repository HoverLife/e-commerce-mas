import asyncio, uuid
from graph.graph import build_chat_graph
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

async def run_cli():
    graph = build_chat_graph()
    session_id = uuid.uuid4().hex
    print("Введите ваш запрос:")
    msg = input("> ")
    state = await graph.ainvoke({
        "messages": [SystemMessage("Доступны инструменты агентам."), HumanMessage(msg)],
        "session_id": session_id,
        "current_item": None,
        "recommended_items": [],
        "final_price": 0.0
    })
    for m in state["messages"]:
        print(f"[{m.role}] {m.content}")

if __name__ == "__main__":
    asyncio.run(run_cli())
