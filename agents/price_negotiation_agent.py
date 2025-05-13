from langchain_core.tools import tool
from typing import List, Dict


@tool
def price_negotiation_agent(item_id: int, current_price: float) -> float:
    """
    Переговоры по цене через GigaChat Function Calling.
    """
    # stub: скидка 5%
    return round(current_price * 0.95, 2)