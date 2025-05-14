from typing import List
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class ChatState(dict):
    """Состояние чата для LangGraph: messages + session_id"""
    pass

# from dataclasses import dataclass, field
# from typing_extensions import Annotated
# from typing import List
# from langgraph.graph import add_messages
# from langchain_core.messages import AnyMessage

# @dataclass
# class ChatState:
#     """
#     Основное состояние переписки в графе.
#     Хранит накопленную историю сообщений.
#     """
#     messages: Annotated[List[AnyMessage], add_messages] = field(default_factory=list)
#     # дополнительные поля, пока не нужны


# # from typing import List, Any
# # from typing_extensions import TypedDict, Annotated
# # from langchain_core.messages import BaseMessage
# # from langgraph.graph import add_messages

# # class ChatState(TypedDict):
# #     """
# #     Состояние графа:
# #       - messages: накопленные сообщения
# #       - session_id: UUID сессии
# #       - current_item: ID выбранного товара
# #       - recommended_items: список ID
# #       - final_price: итоговая цена
# #     """
# #     messages: Annotated[List[BaseMessage], add_messages]
# #     session_id: str
# #     current_item: Any
# #     recommended_items: List[Any]
# #     final_price: float
