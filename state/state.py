# state/state.py
from typing_extensions import TypedDict
from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage

class ChatState(TypedDict):
    messages: list[AnyMessage]  # add_messages аннотируется в graph
    session_id: str
