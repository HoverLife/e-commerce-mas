from typing import Dict, List, Any

async def item_agent(item_id: int, items: List[Dict]) -> Dict[str, Any]:
    """
    Ищет в списке items элемент по id (index).
    """
    for it in items:
        if it.get("id") == item_id:
            return it
    return {}
