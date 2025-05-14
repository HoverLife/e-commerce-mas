# tools/tools.py
from langchain_core.tools import tool
from typing import List, Dict

@tool
async def buyer_agent_tool(preferences: List[str], items: List[Dict]) -> int:
    from agents.buyer_agent import buyer_agent
    return await buyer_agent(preferences, items)

@tool
async def cross_sell_agent_tool(item_id: int) -> List[int]:
    from agents.cross_sell_agent import cross_sell_agent
    return await cross_sell_agent(item_id)

@tool
async def item_agent_tool(item_id: int, items: List[Dict]) -> Dict:
    from agents.item_agent import item_agent
    return await item_agent(item_id, items)

@tool
async def price_negotiation_agent_tool(item_id: int, current_price: float) -> float:
    from agents.price_negotiation_agent import price_negotiation_agent
    return await price_negotiation_agent(item_id, current_price)
