from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from state.state import MessagesState
from configuration.configuration import Configuration
from tools.tools import search_items, get_item_details, cross_sell, negotiate_price
from agents.buyer_agent import buyer_agent
from agents.item_agent import item_agent
from agents.marketplace_agent import marketplace_agent
from agents.cross_sell_agent import cross_sell_agent
from agents.price_negotiation_agent import price_negotiation_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Создаём модель GigaChat
cfg = Configuration()
model = init_chat_model(
    model="GigaChat",
    credentials=cfg.gigi_auth_header,
    scope=cfg.giga_scope,
    verify_ssl_certs=False,
).bind_tools([
    search_items,
    get_item_details,
    cross_sell,
    negotiate_price,
    buyer_agent,
    item_agent,
    marketplace_agent,
    cross_sell_agent,
    price_negotiation_agent,
])

# Строим граф
builder = StateGraph(MessagesState)
builder.add_node("react", lambda state: model.ainvoke([{"role":"user","content":state['user_query']}]))
builder.add_node("tools", ToolNode(model.tools))
builder.add_edge(START, "react")
builder.add_edge("react", "tools")
builder.add_edge("tools", "react")
# можно настроить условие завершения, когда модель возвращает финальное сообщение без вызовов

graph = builder.compile()