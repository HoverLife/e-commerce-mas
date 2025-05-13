from fastapi import FastAPI
from fastapi.responses import JSONResponse
from giga_integration.negotiation_protocol import build_negotiation_graph
from langchain_core.messages import SystemMessage

app = FastAPI()

@app.get("/")
async def root():
    return JSONResponse({"status": "ok", "message": "MAS negotiation API is up."})

@app.post("/simulate")
async def simulate():
    graph = build_negotiation_graph()
    initial_state = {"messages": [], "sender": ""}
    state = await graph.run(initial_state)
    # Собираем только пользовательские сообщения (без SystemMessage)
    chat_history = [m for m in state["messages"] if not isinstance(m, SystemMessage)]
    results = []
    # Чередуем: первые два — от «Buyer», следующие — «Seller»
    for idx, msg in enumerate(chat_history):
        sender = "Buyer" if idx % 2 == 0 else "Seller"
        results.append({"sender": sender, "text": msg.content})
    agreement = any(m["sender"] == "Seller" and "accept" in m["text"].lower()
                    for m in results)
    return {"messages": results, "agreement": agreement}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
