import random
from agents.buyer_agent import BuyerAgent
from agents.item_agent import ItemAgent
from agents.marketplace_agent import MarketplaceAgent
from metrics.evaluation import calculate_ctr


# simulator.py (изменения)
import os
from dotenv import load_dotenv
import os, mysql.connector, logging
import mysql.connector

from agents.cross_sell_agent import CrossSellAgent
from agents.price_negotiation_agent import PriceNegotiationAgent
# ... (существующие импорты BuyerAgent, ItemAgent, MarketplaceAgent и т.д.)

load_dotenv()  # Загружаем .env с данными подключения

# class Simulator:
#     def __init__(self):
#         # Загрузка товаров из удалённой базы данных MariaDB вместо статического списка
#         db_conn = mysql.connector.connect(
#             host=os.getenv("DB_HOST"),
#             port=int(os.getenv("DB_PORT", "3306")),
#             user=os.getenv("DB_USER"),
#             password=os.getenv("DB_PASSWORD"),
#             database=os.getenv("DB_NAME")
#         )

#         cursor = db_conn.cursor()
#         cursor.execute("SELECT Name, Category, Price FROM products_INFORMATION")
#         self.items = []
#         for idx, (name, category, price) in enumerate(cursor.fetchall(), start=1):
#             # Формируем список товаров в формате ItemAgent (id, name, category, price)
#             self.items.append({"id": idx, "name": name, "category": category, "price": price})
#         db_conn.close()

#         # Инициализация существующих агентов
#         self.buyer_agent = BuyerAgent()
#         self.item_agent = ItemAgent()
#         self.marketplace_agent = MarketplaceAgent()
#         # Инициализация новых агентов
#         self.cross_sell_agent = CrossSellAgent()
#         self.price_negotiation_agent = PriceNegotiationAgent()

logger = logging.getLogger(__name__)

class Simulator:
    def __init__(self):
        # Пытаемся загрузить товары из облачной БД
        try:
            conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT", "3306")),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
            )
            cursor = conn.cursor()
            cursor.execute("SELECT Name, Category, Price FROM products_INFORMATION;")
            rows = cursor.fetchall()
            self.items = [
                ItemAgent(i+1, name, category, price)
                for i, (name, category, price) in enumerate(rows)
            ]
            cursor.close()
            conn.close()
            logger.info(f"Загружено {len(self.items)} товаров из БД")
        except Exception as e:
            logger.error(f"Не удалось загрузить из БД, используем жёстко зашитый список: {e}")
            # Фоллбэк
            self.items = [
                ItemAgent(1, "Wireless Mouse", "electronics", 25.99),
                ItemAgent(2, "Python Programming Book", "books", 39.99),
                ItemAgent(3, "Gaming Keyboard", "electronics", 59.99),
                ItemAgent(4, "Sci-Fi Novel", "books", 14.99),
                ItemAgent(5, "Cookware Set", "kitchen", 79.99),
                ItemAgent(6, "Chef Knife", "kitchen", 19.99),
                ItemAgent(7, "Laptop", "electronics", 129.99),
                ItemAgent(8, "Vegetables Knife", "kitchen", 12.99),
                ItemAgent(9, "Laptop", "electronics", 499.99),
                ItemAgent(10, "Headphones", "electronics", 99.99),
                ItemAgent(11, "Shovel", "garden", 14.99),
                ItemAgent(12, "Golden fork", "kitchen", 19.99),
                ItemAgent(13, "Cup", "kitchen", 9.99),
                ItemAgent(14, "Fairy tale", "books", 19.99),
                ItemAgent(15, "Book of receipts", "books", 19.99),
                ItemAgent(16, "Bottle for milk", "kitchen", 7.99),
                ItemAgent(17, "Mobile phone", "electronics", 699.99),
                ItemAgent(18, "Pink T-shirt", "clothes", 19.99),
                ItemAgent(19, "Pan", "kitchen", 19.99),
                ItemAgent(20, "Chef Knife", "kitchen", 19.99),
                ItemAgent(21, "Shoes", "clothes", 49.99),
                ItemAgent(22, "Square Pants", "clothes", 28.99),
                ItemAgent(23, "Candycrush", "games", 29.99),
                ItemAgent(24, "Hat", "clothes", 8.99),
                ItemAgent(25, "Buzyboard", "games", 12.99),
                ItemAgent(26, "Black T-shirt", "clothes", 19.99),
                ItemAgent(27, "Matreshka", "games", 17.99),
                ItemAgent(28, "White T-shirt", "clothes", 19.99)
                # ... остальные ваши тестовые товары
            ]
        self.marketplace = MarketplaceAgent(self.items)

    def run(self):
        # Генерация рекомендаций MarketplaceAgent
        recommended_item = self.marketplace_agent.recommend(self.items)
        # Переговоры о цене до выбора товара
        new_price = self.price_negotiation_agent.negotiate_price(
            recommended_item["name"], recommended_item["category"], recommended_item["price"]
        )
        if new_price != recommended_item["price"]:
            recommended_item["price"] = new_price
            print(f"Цена скорректирована после переговоров: {new_price}")
        # Выбор товара покупателем
        chosen_item = self.buyer_agent.select_item(recommended_item)
        # Предложение кросс-продаж после выбора товара
        cross_ids = self.cross_sell_agent.suggest_additions(chosen_item["name"])
        print(f"Кросс-продажи (ID товаров): {cross_ids}")

    def simulate(self, num_sessions=1):
        sessions_data = []
        last_recs = []
        categories = list({item.category for item in self.items})
        for _ in range(num_sessions):
            buyer = BuyerAgent(random.sample(categories, k=random.randint(1, len(categories))))
            recs = self.marketplace.recommend(buyer)
            clicks = 1 if buyer.choose_item(recs) else 0
            sessions_data.append({"impressions": len(recs), "clicks": clicks})
            last_recs = recs
        ctr = calculate_ctr(sessions_data)
        return last_recs, ctr

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
