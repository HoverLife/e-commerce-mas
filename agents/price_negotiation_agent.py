from langchain_core.tools import tool
from typing import List, Dict


async def price_negotiation_agent(item_id: int, current_price: float) -> float:
    """
    Снижает цену на 5%.
    """
    return round(current_price * 0.95, 2)
