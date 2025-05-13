from typing import List, Dict

async def buyer_agent(preferences: List[str], items: List[Dict]) -> int:
    """
    Выбирает первый товар из списка или -1.
    """
    return items[0]["id"] if items else -1
