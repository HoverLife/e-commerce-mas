import os
import json
import uuid
from datetime import datetime

import aiofiles
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import Response
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from graph.graph import graph
from state.state import ChatState

os.makedirs("dialogues", exist_ok=True)

app = FastAPI(title="MAS with GigaChat Function Calling")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        session_id = uuid.uuid4().hex
        # начальная история
        system_msg = SystemMessage("Ниже идёт диалог. Отвечай через GigaChat, используй функцию fetch_products для БД.")
        human_msg = HumanMessage(req.message)
        state: ChatState = await graph.ainvoke({
            "messages": [system_msg, human_msg]
        })

        # сохраняем историю
        entries = []
        for idx, m in enumerate(state["messages"]):
            from langchain_core.messages import SystemMessage as Sys, HumanMessage as Hum, AIMessage as AIM
            if isinstance(m, Sys):
                role = "system"
            elif isinstance(m, Hum):
                role = "user"
            elif isinstance(m, AIM):
                role = "assistant"
            else:
                role = "tool"
            ent = {
                "id": idx + 1,
                "timestamp": datetime.now().isoformat(),
                "role": role,
                "content": m.content
            }
            if hasattr(m, "tool_calls"):
                ent["tool_calls"] = m.tool_calls
            entries.append(ent)
        path = f"dialogues/session_{session_id}.json"
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(entries, ensure_ascii=False, indent=2))

        # последний ответ AI
        reply = ""
        for m in reversed(state["messages"]):
            if isinstance(m, AIMessage):
                reply = m.content
                break

        return {"session_id": session_id, "response": reply}

    except Exception as e:
        import traceback, sys
        traceback.print_exc(file=sys.stderr)
        return Response(str(e), status_code=500)
