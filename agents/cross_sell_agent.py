import os, logging
from langchain_gigachat import GigaChat
from langchain_core.messages import SystemMessage, HumanMessage
from tools import recommend_items
from langgraph.types import Command

logger = logging.getLogger(__name__)

async def CrossSellAgent(state: dict) -> Command:
    """
    Агент кросс-продажи: рекомендует дополнительные товары.
    Демонстрирует обращение к модели GigaChat (Function Calling).
    """
    item_id = state.get("current_item", "")
    if not item_id:
        logger.info("[CrossSellAgent] Нет выбранного товара для кросс-продажи.")
        return Command(goto=Command.END)
    logger.info(f"[CrossSellAgent] Генерируем рекомендации для товара: {item_id}")

    # Пример использования GigaChat для генерации рекомендаций через функции
    gigachat = GigaChat(verify_ssl_certs=False, credentials=os.environ.get("GIGACHAT_CREDENTIALS"))
    messages = [
        SystemMessage(content="You are a cross-selling assistant."),
        HumanMessage(content=f"Suggest three related items to upsell for item {item_id}.")
    ]
    response = await gigachat.ainvoke(messages)
    recs_str = response.content or ""
    # Пытаемся разбить ответ на список (например через запятую)
    recommended_items = [s.strip() for s in recs_str.split(",") if s.strip()]
    if not recommended_items:
        # Если модель не выдала результат, используем fallback-инструмент
        recommended_items = recommend_items(item_id, 3)
    logger.info(f"[CrossSellAgent] Рекомендованные товары: {recommended_items}")

    # Сохраняем рекомендации и идём к переговорщику
    return Command(goto="PriceNegotiationAgent", update={"recommended_items": recommended_items})
