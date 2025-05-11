# agents/cross_sell_agent.py
import re
from giga_integration.negotiation_protocol import GigaChatNegotiator
from typing import List, Dict

class CrossSellAgent:
    def __init__(self):
        self.negotiator = GigaChatNegotiator()

    def suggest_additions(self, chosen_item_name: str) -> List[int]:
        prompt = (
            f"Покупатель выбрал «{chosen_item_name}». "
            "Что ещё можно ему предложить в дополнение? "
            "Ответь списком ID из доступных товаров, например: 1,2,5."
        )
        response = self.negotiator.ask(prompt)
        # Вытащим все числа из ответа и вернём их как список int
        return [int(num) for num in re.findall(r'\d+', response)]
