import uuid
import aiofiles
import json
from typing import List, Dict
from langchain_core.tools import tool

@tool
async def marketplace_agent_tool(preferences: List[str], limit: int = 0) -> List[Dict]:
    """
    Получает товары по категориям preferences из БД.
    Если limit > 0 — возвращает топ-N самых дешёвых.
    """
    from agents.marketplace_agent import marketplace_agent
    return await marketplace_agent(preferences, limit)

@tool
async def buyer_agent_tool(preferences: List[str], items: List[Dict]) -> int:
    """
    Выбирает товар на основе предпочтений. Возвращает id выбранного товара или -1.
    """
    from agents.buyer_agent import buyer_agent
    return await buyer_agent(preferences, items)

@tool
async def cross_sell_agent_tool(item_id: int) -> List[int]:
    """
    Предлагает два следующих id товаров для кросс-продажи.
    """
    from agents.cross_sell_agent import cross_sell_agent
    return await cross_sell_agent(item_id)

@tool
async def item_agent_tool(item_id: int, items: List[Dict]) -> Dict:
    """
    Возвращает информацию по товару с данным item_id из списка items.
    """
    from agents.item_agent import item_agent
    return await item_agent(item_id, items)

@tool
async def price_negotiation_agent_tool(item_id: int, current_price: float) -> float:
    """
    Снижает текущую цену на 5% и возвращает новую цену.
    """
    from agents.price_negotiation_agent import price_negotiation_agent
    return await price_negotiation_agent(item_id, current_price)
