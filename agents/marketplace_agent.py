# agents/marketplace_agent.py
import asyncpg
from typing import List, Dict, Optional
from config.configuration import Settings

_pool: Optional[asyncpg.Pool] = None

async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        cfg = Settings()
        _pool = await asyncpg.create_pool(
            host=cfg.DB_HOST,
            port=cfg.DB_PORT,
            user=cfg.DB_USER,
            password=cfg.DB_PASSWORD,
            database=cfg.DB_NAME,
            min_size=1,
            max_size=10
        )
    return _pool

async def marketplace_agent(
    preferences: List[str],
    limit: int = 0
) -> List[Dict]:
    pool = await get_pool()
    sql = "SELECT name, category, price FROM products WHERE category = ANY($1::text[])"
    if limit > 0:
        sql += " ORDER BY price ASC LIMIT $2"
        rows = await pool.fetch(sql, preferences, limit)
    else:
        rows = await pool.fetch(sql, preferences)

    return [
        {"id": idx+1, "name": r["name"], "category": r["category"], "price": float(r["price"])}
        for idx, r in enumerate(rows)
    ]
