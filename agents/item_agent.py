import logging
from langgraph.types import Command

logger = logging.getLogger(__name__)

async def ItemAgent(state: dict) -> Command:
    """
    Агент, отвечающий за выбор конкретного товара из списка.
    Берёт первый товар из найденных marketplace и передаёт его дальше.
    """
    items = state.get("items", [])
    if not items:
        logger.info("[ItemAgent] Нет доступных товаров, завершаем процесс.")
        return Command(goto=Command.END)  # Если нет товаров, завершаем
    current_item = items[0]
    item_id = current_item.get("id")
    logger.info(f"[ItemAgent] Выбран товар: {item_id}")
    # Сохраняем выбранный товар и идём к CrossSellAgent
    return Command(goto="CrossSellAgent", update={"current_item": item_id})
