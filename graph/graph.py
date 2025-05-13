import json
import uuid
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from state.state import MessagesState
from tools.tools import (
    buyer_agent,
    marketplace_agent,
    item_agent,
    cross_sell_agent,
    price_negotiation_agent,
    get_dialogue_history,
)
from utils.gigachat import GigaChatClient

def build_chat_graph() -> StateGraph:
    client = GigaChatClient()
    tools = [
        buyer_agent,
        marketplace_agent,
        item_agent,
        cross_sell_agent,
        price_negotiation_agent,
        get_dialogue_history,
    ]
    tool_node = ToolNode(tools)

    async def call_model(state: MessagesState) -> dict:
        # Преобразуем BaseMessage в dict API
        api_msgs = []
        for m in state["messages"]:
            api_msgs.append({"role": m.role, "content": m.content})
        js = await client.chat(api_msgs)
        choice = js["choices"][0]["message"]
        content = choice.get("content", "")
        fc = choice.get("function_call")
        if fc:
            name = fc["name"]
            args = json.loads(fc.get("arguments", "{}"))
            tc = {"id": str(uuid.uuid4()), "name": name, "args": args}
            return {"messages": [AIMessage("", tool_calls=[tc])]}
        return {"messages": [AIMessage(content)]}

    graph = StateGraph(MessagesState)
    graph.add_node("model", call_model)
    graph.add_node("action", tool_node)
    graph.add_edge(START, "model")
    graph.add_conditional_edges(
        "model",
        lambda s: "action" if isinstance(s["messages"][-1], AIMessage) and getattr(s["messages"][-1], "tool_calls", None) else END,
        {"action": "action", END: END}
    )
    graph.add_edge("action", "model")
    return graph.compile()
