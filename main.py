import uvicorn
from fastapi import FastAPI
from graph.graph import graph
from state.state import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage

app = FastAPI()

@app.get("/")
def root():
    return {"status":"ok","message":"MAS ready"}

@app.post("/simulate")
async def simulate(preferences: list[str]):
    # Инициализируем состояние
    state: MessagesState = {"messages": [], "current_item": None, "recommended_items": [], "final_price": 0.0, 'user_query': ' '.join(preferences)}
    out = await graph.invoke(state)
    # Собираем текст ответов
    return {"state": out}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)