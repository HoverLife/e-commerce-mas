# tools/db_tools.py

from typing import List, Dict
from langchain_core.tools import BaseTool, ToolException

class FetchProductsTool(BaseTool):
    # Поля должны быть аннотированы, иначе Pydantic жалуется
    name: str = "fetch_products"
    description: str = "Fetch products from the database by category."
    args_schema: Dict = {
        "type": "object",
        "properties": {
            "category": {"type": "string"},
            "limit": {"type": "integer", "default": 0}
        },
        "required": ["category"]
    }

    async def _run(self, category: str, limit: int = 0) -> List[Dict]:
        from agents.marketplace_agent import marketplace_agent
        return await marketplace_agent([category], limit)

    async def _arun(self, *args, **kwargs):
        raise ToolException("Sync run not supported")

# Экспортируем список инструментов
TOOLS: List[BaseTool] = [FetchProductsTool()]
