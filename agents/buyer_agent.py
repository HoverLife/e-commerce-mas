class BuyerAgent:
    """
    Агент-покупатель с предпочтениями и выбором товаров.
    """
    def __init__(self, preferences):
        self.preferences = preferences

    def choose_item(self, recommendations):
        """
        Выбирает первый товар из списка рекомендаций.
        """
        if recommendations:
            return recommendations[0]
        return None
