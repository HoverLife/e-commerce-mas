from typing import List, Dict
from langchain_core.tools import tool

@tool
def search_items(preferences: List[str], items: List[Dict]) -> List[int]:
    """
    Возвращает ID товаров, соответствующих предпочтениям.
    """
    return [item['id'] for item in items if item['category'] in preferences]

@tool
def get_item_details(item_id: int, items: List[Dict]) -> Dict:
    """
    Получить детали товара (price, category).
    """
    for it in items:
        if it['id'] == item_id:
            return it
    return {}

@tool
def cross_sell(item_id: int) -> List[int]:
    """
    Рекомендует ID дополнительных товаров.
    """
    # stub: +1, +2 модифицированные
    return [item_id + 1, item_id + 2]

@tool
def negotiate_price(item_id: int, current_price: float) -> float:
    """
    Предлагает новую цену (скидка 10%).
    """
    return round(current_price * 0.9, 2)