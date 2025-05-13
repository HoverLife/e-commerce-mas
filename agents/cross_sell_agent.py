from langchain_core.tools import tool
from typing import List


@tool
def cross_sell_agent(item_id: int) -> List[int]:
    """
    Кросс-продажа для выбранного товара.
    """
    # Здесь можно поднять GigaChat Function Calling
    return [item_id + 1, item_id + 2]