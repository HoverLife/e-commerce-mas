from typing import List, Dict
# Импортируем из langchain_community, а не из langchain.tools
from langchain_core.tools import BaseTool
from langchain_core.tools import ToolException


class FetchProductsTool(BaseTool):
    name: str = "fetch_products"
    description: str = (
        "Fetch products from the database by category. "
        "Return list of {id, name, category, price}. "
        "Optional `limit` to get top‑N cheapest."
    )
    args_schema = {
        "type": "object",
        "properties": {
            "category": {"type": "string", "description": "Category name"},
            "limit": {"type": "integer", "description": "Max items, sorted by price asc", "default": 0},
        },
        "required": ["category"]
    }

    async def _run(self, category: str, limit: int = 0) -> List[Dict]:
        from agents.marketplace_agent import marketplace_agent
        items = await marketplace_agent([category], limit=limit)
        return items

    async def _arun(self, *args, **kwargs):
        raise ToolException("Sync run not supported")

# Экспортируем список инструментов
TOOLS = [FetchProductsTool()]


# # tools/db_tools.py
# from typing import List, Dict
# from langchain.tools import BaseTool, ToolException

# class FetchProductsTool(BaseTool):
#     name = "fetch_products"
#     description = (
#         "Fetch products from the database by category. "
#         "Returns a list of items with id, name, category, price. "
#         "You can pass `limit` to get only top-N items sorted by price ascending."
#     )

#     # JSON‑схема для аргументов
#     args_schema = {
#         "type": "object",
#         "properties": {
#             "category": {"type": "string", "description": "Product category to filter"},
#             "limit": {
#                 "type": "integer",
#                 "description": "Maximum number of items to return (sorted by price asc)",
#                 "default": 0
#             }
#         },
#         "required": ["category"]
#     }

#     async def _run(self, category: str, limit: int = 0) -> List[Dict]:
#         """
#         Вызывается, когда LLM делает function_call.
#         """
#         from agents.marketplace_agent import marketplace_agent
#         items = await marketplace_agent([category])
#         if limit and isinstance(limit, int) and limit > 0:
#             items = sorted(items, key=lambda x: x["price"])[:limit]
#         return items

#     async def _arun(self, *args, **kwargs):
#         # no sync support
#         raise ToolException("FetchProductsTool does not support sync")

# # Экспортируем список инструментов
# TOOLS = [FetchProductsTool()]
