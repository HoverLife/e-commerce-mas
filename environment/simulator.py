import asyncio
from negotiation_protocol import build_negotiation_graph

async def simulate_session():
    graph = build_negotiation_graph()
    initial_state = {"messages": [], "sender": ""}
    final_state = await graph.run(initial_state)
    return final_state

async def simulate_sessions(n_sessions: int = 1):
    sessions = [simulate_session() for _ in range(n_sessions)]
    return await asyncio.gather(*sessions)

if __name__ == "__main__":
    # Example: run 3 simulated buyer sessions
    results = asyncio.run(simulate_sessions(3))
    for i, session in enumerate(results, 1):
        print(f"Session {i}:")
        for msg in session["messages"]:
            content = msg.content if hasattr(msg, "content") else ""
            print(content)
        print("-" * 20)


# class Simulator:
#     """
#     Симулятор нескольких сессий взаимодействия покупателей и рынка.
#     """
#     def __init__(self):
#         # Создаём примеры товаров в магазине
#         self.items = [
#             ItemAgent(1, "Wireless Mouse", "electronics", 25.99),
#             ItemAgent(2, "Python Programming Book", "books", 39.99),
#             ItemAgent(3, "Gaming Keyboard", "electronics", 59.99),
#             ItemAgent(4, "Sci-Fi Novel", "books", 14.99),
#             ItemAgent(5, "Cookware Set", "kitchen", 79.99),
#             ItemAgent(6, "Chef Knife", "kitchen", 19.99),
#             ItemAgent(7, "Laptop", "electronics", 129.99),
#             ItemAgent(8, "Vegetables Knife", "kitchen", 12.99),
#             ItemAgent(9, "Laptop", "electronics", 499.99),
#             ItemAgent(10, "Headphones", "electronics", 99.99),
#             ItemAgent(11, "Shovel", "garden", 14.99),
#             ItemAgent(12, "Golden fork", "kitchen", 19.99),
#             ItemAgent(13, "Cup", "kitchen", 9.99),
#             ItemAgent(14, "Fairy tale", "books", 19.99),
#             ItemAgent(15, "Book of receipts", "books", 19.99),
#             ItemAgent(16, "Bottle for milk", "kitchen", 7.99),
#             ItemAgent(17, "Mobile phone", "electronics", 699.99),
#             ItemAgent(18, "Pink T-shirt", "clothes", 19.99),
#             ItemAgent(19, "Pan", "kitchen", 19.99),
#             ItemAgent(20, "Chef Knife", "kitchen", 19.99),
#             ItemAgent(21, "Shoes", "clothes", 49.99),
#             ItemAgent(22, "Square Pants", "clothes", 28.99),
#             ItemAgent(23, "Candycrush", "games", 29.99),
#             ItemAgent(24, "Hat", "clothes", 8.99),
#             ItemAgent(25, "Buzyboard", "games", 12.99),
#             ItemAgent(26, "Black T-shirt", "clothes", 19.99),
#             ItemAgent(27, "Matreshka", "games", 17.99),
#             ItemAgent(28, "White T-shirt", "clothes", 19.99)
#         ]
#         self.marketplace = MarketplaceAgent(self.items)

#     def simulate(self, num_sessions=1):
#         """
#         Проводит симуляцию заданного количества сессий.
#         Возвращает рекомендации последней сессии и общий CTR.
#         """
#         sessions_data = []
#         last_recommendations = []
#         categories = list({item.category for item in self.items})
#         for _ in range(num_sessions):
#             # Создаём покупателя с случайными предпочтениями
#             num_pref = random.randint(1, len(categories))
#             preferences = random.sample(categories, k=num_pref)
#             buyer = BuyerAgent(preferences)
#             # Получаем рекомендации и симулируем выбор первого товара
#             recommendations = self.marketplace.recommend(buyer)
#             chosen = buyer.choose_item(recommendations)
#             impressions = len(recommendations)
#             clicks = 1 if chosen else 0
#             sessions_data.append({"impressions": impressions, "clicks": clicks})
#             last_recommendations = recommendations
#         ctr = calculate_ctr(sessions_data)
#         return last_recommendations, ctr
