import asyncio
from graph.graph import build_chat_graph

async def run_cli():
    msg = input("Введите сообщение пользователю: ")
    graph = build_chat_graph()
    state = await graph.ainvoke({"messages": [], "user_query": msg, "current_item": None, "recommended_items": [], "final_price": 0.0})
    for m in state["messages"]:
        print(f"{m.role}: {m.content}")

if __name__ == "__main__":
    asyncio.run(run_cli())
