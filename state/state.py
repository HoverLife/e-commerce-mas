from typing import List, TypedDict, Any
from langchain_core.messages import BaseMessage

class MessagesState(TypedDict):
    messages: List[BaseMessage]
    current_item: Any
    recommended_items: List[Any]
    final_price: float