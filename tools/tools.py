# tools/tools.py

import json
from langchain_core.tools import tool

@tool
async def buyer_agent(prompt: str) -> str:
    """
    Агент-покупатель.
    
    Args:
        prompt: Текст, описывающий текущее предложение или рекомендации.
    Returns:
        Ответ от BuyerAgent на основе входного prompt.
    """
    return f"BuyerAgent получил: «{prompt}»."

@tool
async def marketplace_agent(prompt: str) -> str:
    """
    Агент-рынок.
    
    Args:
        prompt: Запрос покупателя или контекст (например, предпочтения).
    Returns:
        Ответ MarketplaceAgent с перечнем подходящих товаров.
    """
    return f"MarketplaceAgent обработал: «{prompt}»."

@tool
async def item_agent(prompt: str) -> str:
    """
    Агент-товар.
    
    Args:
        prompt: ID или имя товара.
    Returns:
        Детали выбранного товара.
    """
    return f"ItemAgent детали для: «{prompt}»."

@tool
async def cross_sell_agent(prompt: str) -> str:
    """
    Агент кросс-продажи.
    
    Args:
        prompt: ID или имя основного товара.
    Returns:
        Предложение сопутствующих товаров.
    """
    return f"CrossSellAgent рекомендует для «{prompt}» дополнительные товары."

@tool
async def price_negotiation_agent(prompt: str) -> str:
    """
    Агент переговоров по цене.
    
    Args:
        prompt: Информация о цене или запрос о скидке.
    Returns:
        Итоговое предложение по цене.
    """
    return f"PriceNegotiationAgent обсудил цену по «{prompt}»."

@tool
async def get_dialogue_history(history_id: str) -> str:
    """
    Инструмент: загрузить историю диалога по идентификатору.
    
    Читает файл `dialogues/history_{history_id}.json`.

    Args:
        history_id: Метка времени или имя файла с историей.
    Returns:
        Содержимое файла истории или сообщение об ошибке.
    """
    filepath = f"dialogues/history_{history_id}.json"
    try:
        async with open(filepath, 'r', encoding='utf-8') as f:
            data = await f.read()
        return f"История (ID={history_id}):\n{data}"
    except FileNotFoundError:
        return f"История с ID={history_id} не найдена."
