# tools/db_tools.py

from typing import List, Dict, Any
from langchain_core.tools import BaseTool, ToolException

class FetchProductsTool(BaseTool):
    """
    Инструмент для получения товаров из PostgreSQL по категории.
    """
    name: str = "fetch_products"
    description: str = (
        "Fetch products from the database by category. "
        "Принимает `category` (string) и `limit` (integer). "
        "Возвращает список объектов {id, name, category, price}."
    )
    args_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "category": {"type": "string", "description": "Category name"},
            "limit": {
                "type": "integer",
                "description": "Max items, sorted by price ascending",
                "default": 0,
            },
        },
        "required": ["category"],
    }

    async def _run(self, category: str, limit: int = 0) -> List[Dict[str, Any]]:
        from agents.marketplace_agent import marketplace_agent
        items = await marketplace_agent([category], limit)
        return items

    async def _arun(self, *args, **kwargs):
        raise ToolException("Synchronous run not supported")
