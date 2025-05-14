import os
import json
import uuid
from datetime import datetime
import logging
import aiofiles
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from graph.graph import graph
from state.state import ChatState

# Настройка логирования
logger = logging.getLogger("agent_actions")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("agent_actions.log", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)

os.makedirs("dialogues", exist_ok=True)
app = FastAPI(title="MAS with GigaChat Function Calling")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    session_id = uuid.uuid4().hex
    system_msg = SystemMessage("Ниже идёт диалог. Отвечай через GigaChat, используй функцию fetch_products для БД.")
    human_msg = HumanMessage(req.message)

    try:
        state: ChatState = await graph.ainvoke({
            "messages": [system_msg, human_msg],
            "session_id": session_id
        })
    except Exception as e:
        logger.exception(f"Graph invocation failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    # Сохраняем историю диалога
    history = []
    for idx, m in enumerate(state.messages):
        if isinstance(m, SystemMessage): role = "system"
        elif isinstance(m, HumanMessage): role = "user"
        elif isinstance(m, AIMessage): role = "assistant"
        else: role = "tool"
        history.append({
            "id": idx + 1,
            "timestamp": datetime.utcnow().isoformat(),
            "role": role,
            "content": m.content
        })
    history_path = f"dialogues/session_{state.session_id}.json"
    try:
        async with aiofiles.open(history_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(history, ensure_ascii=False, indent=2))
    except Exception:
        logger.exception("Failed to write dialogue history")

    # Логируем действия
    user_text = req.message
    ai_text = next((m.content for m in reversed(state.messages) if isinstance(m, AIMessage)), "")
    logger.info(f"[session:{state.session_id}] User: {user_text}")
    logger.info(f"[session:{state.session_id}] Agent: {ai_text}")

    return {"session_id": state.session_id, "response": ai_text}