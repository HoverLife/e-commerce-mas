import os, logging
from langchain_gigachat import GigaChat
from langchain_core.messages import SystemMessage, HumanMessage
from tools import negotiate_price, get_item_details
from langgraph.types import Command

logger = logging.getLogger(__name__)

async def PriceNegotiationAgent(state: dict) -> Command:
    """
    Агент переговоров по цене: устанавливает финальную цену для товара.
    Демонстрирует обращение к GigaChat (Function Calling) и инструментам.
    """
    item_id = state.get("current_item", "")
    if not item_id:
        logger.info("[PriceNegotiationAgent] Нет товара для переговоров.")
        return Command(goto=Command.END)
    details = get_item_details(item_id)
    current_price = details.get("price", 0.0)
    logger.info(f"[PriceNegotiationAgent] Начальная цена товара {item_id}: {current_price}")

    # Пример использования GigaChat для переговоров по цене через функцию
    gigachat = GigaChat(verify_ssl_certs=False, credentials=os.environ.get("GIGACHAT_CREDENTIALS"))
    messages = [
        SystemMessage(content="You are a pricing agent."),
        HumanMessage(content=f"The buyer wants item {item_id} at price {current_price}. Provide a final agreed price or counter-offer.")
    ]
    response = await gigachat.ainvoke(messages)
    price_str = response.content.strip() if response.content else ""
    try:
        final_price = float(price_str)
    except ValueError:
        # Если парсинг не удался, используем fallback-инструмент
        final_price = negotiate_price(item_id, current_price)
    logger.info(f"[PriceNegotiationAgent] Итоговая цена для товара {item_id}: {final_price}")

    # Завершаем работу, сохраняя финальную цену
    return Command(goto=Command.END, update={"final_price": final_price})
