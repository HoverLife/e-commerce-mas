# agents/price_negotiation_agent.py
import re
from giga_integration.negotiation_protocol import GigaChatNegotiator

class PriceNegotiationAgent:
    def __init__(self):
        self.negotiator = GigaChatNegotiator()

    def negotiate_price(self, item_name: str, category: str, price: int) -> int:
        prompt = (
            f"Покупателю рекомендован товар «{item_name}» "
            f"из категории {category} за цену {price}. "
            "Справедлива ли цена и какую цену лучше предложить? "
            "Ответь новым значением цены или «OK»."
        )
        response = self.negotiator.ask(prompt)
        # Если где-то есть число — считаем это новой ценой
        match = re.search(r'\d+', response)
        return int(match.group()) if match else price
