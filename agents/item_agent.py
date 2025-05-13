from langchain_core.tools import tool
from typing import Dict, List

@tool
def item_agent(item_id: int, items: List[Dict]) -> Dict:
    """
    Возвращает детали выбранного товара.
    """
    for it in items:
        if it['id'] == item_id:
            return it
    return {}