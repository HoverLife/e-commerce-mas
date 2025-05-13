from typing import List, TypedDict, Any
from langchain_core.messages import BaseMessage
from typing_extensions import Annotated
from langgraph.graph import add_messages

class MessagesState(TypedDict):
    """
    Состояние графа: накапливает историю сообщений и хранит ответ сервиса.
    """
    messages: Annotated[List[BaseMessage], add_messages]
    user_query: str
    current_item: Any
    recommended_items: List[Any]
    final_price: float
