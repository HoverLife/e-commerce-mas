from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from typing import List, Dict

@tool
def buyer_agent(preferences: List[str], items: List[Dict]) -> int:
    """
    Выбирает первый товар из рекомендаций.
    """
    if items:
        return items[0]['id']
    return -1