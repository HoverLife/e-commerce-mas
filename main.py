import os
import uuid
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from graph.graph import graph  # ваш LangGraph
from langchain_core.messages import AIMessage

# ─── Логирование ────────────────────────────────
logger = logging.getLogger("mas_app")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("agent_actions.log", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(fh)

app = FastAPI(title="MAS Orchestrator with LangGraph")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    session_id = uuid.uuid4().hex
    user_text = req.message.strip()
    logger.info(f"[{session_id}] User: {user_text}")

    # 1) Подготовка входа для графа
    system_msg = {
        "role": "system",
        "content": "Ты — ассистент с функцией fetch_products(category, limit) для работы с БД."
    }
    user_msg = {"role": "user", "content": user_text}

    try:
        # 2) Асинхронный вызов графа
        result = await graph.ainvoke({"messages": [system_msg, user_msg]})
    except Exception as e:
        logger.exception(f"[{session_id}] Graph error")
        raise HTTPException(500, "Internal agent error")

    # 3) Проверяем результат
    if not isinstance(result, dict) or "messages" not in result:
        logger.error(f"[{session_id}] Unexpected graph output: {result!r}")
        raise HTTPException(500, "Unexpected agent output")

    # 4) Извлекаем ответ от ассистента
    reply = None
    for m in reversed(result["messages"]):
        if m.get("role") == "assistant" and "content" in m:
            reply = m["content"]
            break

    if reply is None:
        logger.error(f"[{session_id}] No assistant message in output")
        raise HTTPException(500, "No response from agent")

    logger.info(f"[{session_id}] Reply: {reply}")
    return {"session_id": session_id, "response": reply}
