import os
import json
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from config.configuration import Configuration
from graph.graph import build_chat_graph

os.makedirs("dialogues", exist_ok=True)
app = FastAPI(title="MAS Chat API")
graph = build_chat_graph()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    init = [SystemMessage("Доступны инструменты агентам."), HumanMessage(req.message)]
    state = await graph.ainvoke({"messages": init, "user_query": req.message, "current_item": None, "recommended_items": [], "final_price": 0.0})
    # Сохраняем историю
    msgs = []
    for m in state["messages"]:
        role = m.role if hasattr(m, "role") else "assistant"
        entry = {"role": role, "content": m.content}
        if hasattr(m, "tool_calls") and m.tool_calls:
            entry["tool_calls"] = m.tool_calls
        msgs.append(entry)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"dialogues/history_{ts}.json"
    async with open(path, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(msgs, ensure_ascii=False, indent=2))
    # Последний ответ AI
    for m in reversed(state["messages"]):
        if isinstance(m, AIMessage):
            return {"response": m.content}
    return {"response": ""}

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "E-commerce multi-agent system is running"}
