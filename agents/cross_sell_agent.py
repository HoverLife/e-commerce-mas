from langchain_core.tools import tool
from typing import List


async def cross_sell_agent(item_id: int) -> List[int]:
    """
    Статичный stub: предлагает два следующих ID.
    """
    return [item_id + 1, item_id + 2]
