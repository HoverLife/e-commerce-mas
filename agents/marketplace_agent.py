from langchain_core.tools import tool
from config.configuration import Configuration
import mysql.connector
from typing import List, Dict

@tool
def marketplace_agent(preferences: List[str]) -> List[Dict]:
    """
    Из БД или фолбека возвращает все товары по предпочтениям.
    """
    cfg = Configuration()
    try:
        conn = mysql.connector.connect(
            host=cfg.db_host,
            port=cfg.db_port,
            user=cfg.db_user,
            password=cfg.db_password,
            database=cfg.db_name,
        )
        cursor = conn.cursor()
        cursor.execute("SELECT name, category, price FROM products_INFORMATION;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        items = [
            {'name': r[1], 'category': r[2], 'price': float(r[3]) }
            for r in rows
        ]
    except Exception:
        # фолбек
        items = [
            {'name': 'Wireless Mouse', 'category': 'electronics', 'price': 25.99 },
            {'name': 'Wireless Mouse', 'category': 'electronics', 'price': 25.99 },
            {'name': 'Wireless Mouse', 'category': 'electronics', 'price': 25.99 },
            {'name': 'Wireless Mouse', 'category': 'electronics', 'price': 25.99 },
            {'name': 'Wireless Mouse', 'category': 'electronics', 'price': 25.99 },
            {'name': 'Wireless Mouse', 'category': 'electronics', 'price': 25.99 },
            {'name': 'Wireless Mouse', 'category': 'electronics', 'price': 25.99 },
            {'name': 'Wireless Mouse', 'category': 'electronics', 'price': 25.99 },
            {'name': 'Wireless Mouse', 'category': 'electronics', 'price': 25.99 },
            {'name': 'Wireless Mouse', 'category': 'electronics', 'price': 25.99 }
            # ... другие
        ]
    # фильтруем по категориям
    return [it for it in items if it['category'] in preferences]