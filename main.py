# main.py
import re
import uuid
import json
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agents.marketplace_agent import marketplace_agent
from agents.buyer_agent import buyer_agent
from agents.cross_sell_agent import cross_sell_agent
from agents.item_agent import item_agent
from agents.price_negotiation_agent import price_negotiation_agent

# ─── Логирование ───────────────────────────────────────────
logger = logging.getLogger("mas")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("agent_actions.log", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(fh)

# ─── Приложение ────────────────────────────────────────────
app = FastAPI(title="MAS Direct Orchestrator")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    # 1) Распарсить категорию
    m = re.search(r"категори[яи]\s+([A-Za-z0-9_]+)", req.message, flags=re.IGNORECASE)
    if not m:
        raise HTTPException(400, detail="Неправильный формат: Покажи товары категории <имя>")
    category = m.group(1).lower()
    session_id = uuid.uuid4().hex

    logger.info(f"[{session_id}] Шаг 1: marketplace_agent({category})")
    try:
        products = await marketplace_agent([category])
    except Exception as e:
        logger.exception(f"[{session_id}] Ошибка на marketplace_agent")
        raise HTTPException(500, detail="Ошибка доступа к базе данных")

    # 2) buyer_agent выбирает один товар
    logger.info(f"[{session_id}] Шаг 2: buyer_agent, {len(products)} items")
    chosen_id = await buyer_agent([category], products)

    # 3) cross_sell_agent предлагает доп. товары
    logger.info(f"[{session_id}] Шаг 3: cross_sell_agent({chosen_id})")
    rec_ids = await cross_sell_agent(chosen_id)

    # 4) item_agent подгружает детали
    logger.info(f"[{session_id}] Шаг 4: item_agent for {rec_ids}")
    rec_items = []
    for rid in rec_ids:
        it = await item_agent(rid, products)
        if it:
            rec_items.append(it)

    # 5) price_negotiation_agent снижает цену у первого рекомендованного
    final_price = None
    if rec_items:
        logger.info(f"[{session_id}] Шаг 5: price_negotiation_agent on {rec_items[0]['id']}")
        final_price = await price_negotiation_agent(
            rec_items[0]["id"], rec_items[0]["price"]
        )

    # Сохранить историю
    hist = {
        "session_id": session_id,
        "category": category,
        "all_products": products,
        "chosen_id": chosen_id,
        "recommended": rec_items,
        "final_price": final_price
    }
    with open(f"dialogues/session_{session_id}.json", "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)

    # Итоговый ответ
    return hist
