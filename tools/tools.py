# tools/tools.py
import aiofiles
import json
import uuid
from typing import List, Dict
from langchain_core.tools import tool


@tool
async def buyer_agent_tool(preferences: List[str], items: List[Dict]) -> int:
    """Tool-обёртка для buyer_agent."""
    from agents.buyer_agent import buyer_agent
    return await buyer_agent(preferences, items)


@tool
async def marketplace_agent_tool(preferences: List[str]) -> List[Dict]:
    """Tool-обёртка для marketplace_agent."""
    from agents.marketplace_agent import marketplace_agent
    return await marketplace_agent(preferences)

@tool
async def item_agent_tool(item_id: int, items: List[Dict]) -> Dict:
    """Tool-обёртка для item_agent."""
    from agents.item_agent import item_agent
    return await item_agent(item_id, items)

@tool
async def cross_sell_agent_tool(item_id: int) -> List[int]:
    """Tool-обёртка для cross_sell_agent."""
    from agents.cross_sell_agent import cross_sell_agent
    return await cross_sell_agent(item_id)

@tool
async def price_negotiation_agent_tool(item_id: int, current_price: float) -> float:
    """Tool-обёртка для price_negotiation_agent."""
    from agents.price_negotiation_agent import price_negotiation_agent
    return await price_negotiation_agent(item_id, current_price)

@tool
async def get_dialogue_history(session_id: str) -> str:
    """
    Загружает JSON истории диалога по session_id.
    """
    path = f"dialogues/session_{session_id}.json"
    try:
        async with aiofiles.open(path, 'r', encoding='utf-8') as f:
            data = await f.read()
        return data
    except FileNotFoundError:
        return "{}"