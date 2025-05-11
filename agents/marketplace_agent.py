# agents/marketplace_agent.py
from giga_integration.negotiation_protocol import get_recommendations

class MarketplaceAgent:
    """
    Агент-рынок: хранит список товаров и генерирует рекомендации для покупателя.
    """
    def __init__(self, items):
        self.items = items

    def recommend(self, buyer_agent):
        preferences = buyer_agent.preferences
        try:
            rec_ids = get_recommendations(preferences, self.items)
        except Exception:
            rec_ids = []
        rec_items = []
        for rec_id in rec_ids:
            for item in self.items:
                if item.id == rec_id:
                    rec_items.append(item)
                    break
        return rec_items
