import logging
from langgraph.types import Command

logger = logging.getLogger(__name__)

async def BuyerAgent(state: dict) -> Command:
    """
    Агент-покупатель: получает запрос покупателя и передаёт управление на маркетплейс.
    """
    buyer_input = state.get("buyer_input", "")
    logger.info(f"[BuyerAgent] Инициализация запроса покупателя: {buyer_input}")
    # Переходим к MarketplaceAgent для обработки запроса
    return Command(goto="MarketplaceAgent")
