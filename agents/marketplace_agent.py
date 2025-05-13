import logging
from langchain.tools import tool
from langgraph.types import Command
from tools import search_items, get_item_details

logger = logging.getLogger(__name__)

async def MarketplaceAgent(state: dict) -> Command:
    """
    Агент-маркетплейс: осуществляет поиск товаров по запросу покупателя.
    Использует инструмент search_items.
    """
    buyer_input = state.get("buyer_input", "")
    logger.info(f"[MarketplaceAgent] Выполняем поиск товаров для запроса: {buyer_input}")
    # Поиск товаров по запросу
    items = search_items(buyer_input)
    # Возможно, обновляем состояние деталями первого товара
    if items:
        first_item = items[0]
        details = get_item_details(first_item["id"])
        # Сохраняем цену или другие характеристики при необходимости
        state.setdefault("item_details", {})[first_item["id"]] = details
        logger.info(f"[MarketplaceAgent] Получены детали для товара {first_item['id']}: {details}")
    else:
        logger.info("[MarketplaceAgent] Товары не найдены.")
    # Переходим к Agent выбора товара
    return Command(goto="ItemAgent", update={"items": items})
