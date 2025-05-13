# giga_integration/negotiation_protocol.py
import re
from typing import TypedDict
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langchain_gigachat import GigaChat

# Initialize GigaChat model (credentials via environment GIGACHAT_CREDENTIALS)
giga_chat = GigaChat(verify_ssl_certs=False, scope="GIGACHAT_API_PERS")

# Tools for negotiation
@tool
def evaluate_offer(price: float, threshold: float = 80.0) -> bool:
    """Return True if price >= threshold."""
    return price >= threshold

@tool
def adjust_price(price: float) -> float:
    """Increase price by 10%."""
    return price * 1.1

# State schema for the graph
class ChatState(TypedDict):
    messages: list[BaseMessage]
    sender: str

async def buyer_agent(state: ChatState):
    # Initialize conversation if first message
    if not state.get("messages"):
        state["messages"] = []
        state["sender"] = ""
    # Buyer makes an initial offer
    offer = 100.0
    buyer_msg = HumanMessage(content=f"My offer is {offer} dollars.")
    state["messages"].append(buyer_msg)
    state["sender"] = "buyer"
    # Log buyer message
    with open("agent_log.txt", "a", encoding="utf-8") as log:
        log.write(f"Buyer: {buyer_msg.content}\n")
    # GigaChat may respond (simulate buyer's follow-up)
    response = await giga_chat.ainvoke(state["messages"])
    state["messages"].append(response)
    # Log buyer follow-up (LLM response)
    with open("agent_log.txt", "a", encoding="utf-8") as log:
        log.write(f"Buyer: {response.content}\n")
    return state

async def seller_agent(state: ChatState):
    # Seller reviews the last buyer message (offer)
    state["messages"].append(SystemMessage(content="You are a seller negotiating for a product."))
    last_msg = state["messages"][-2] if len(state["messages"]) >= 2 else None
    text = last_msg.content if last_msg else ""
    price_match = re.search(r"\d+(?:\.\d+)?", text)
    buyer_price = float(price_match.group()) if price_match else 0.0
    # Evaluate offer
    if evaluate_offer(price=buyer_price):
        reply = "Deal! I accept your offer."
    else:
        counter = adjust_price(price=buyer_price)
        reply = f"I cannot accept that. My counteroffer is {counter:.2f} dollars."
    seller_msg = HumanMessage(content=reply)
    state["messages"].append(seller_msg)
    state["sender"] = "seller"
    # Log seller response
    with open("agent_log.txt", "a", encoding="utf-8") as log:
        log.write(f"Seller: {reply}\n")
    return state

def build_negotiation_graph():
    graph = StateGraph(ChatState)
    graph.add_node("buyer", buyer_agent)
    graph.add_node("seller", seller_agent)
    graph.add_edge("buyer", "seller")
    graph.add_edge("seller", END)
    return graph

    




#     # giga_integration/negotiation_protocol.py
# import os
# import json
# import uuid
# import requests
# import logging
# import urllib3

# # Отключаем предупреждения про self‑signed SSL
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("negotiation_protocol")

# def get_oauth_token():
#     auth_token = os.getenv("GIGA_AUTH_HEADER")
#     scope = os.getenv("GIGA_SCOPE", "GIGACHAT_API_PERS")
#     if not auth_token:
#         logger.warning("GIGA_AUTH_HEADER не задан — пропускаем OAuth")
#         return None

#     url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Accept": "application/json",
#         "RqUID": str(uuid.uuid4()),
#         "Authorization": f"Basic {auth_token}"
#     }
#     data = {"scope": scope}

#     try:
#         resp = requests.post(url, headers=headers, data=data, timeout=5, verify=False)
#         resp.raise_for_status()
#         token = resp.json().get("access_token")
#         logger.info(f"Получен OAuth‑токен: {token[:10]}…")
#         return token
#     except Exception as e:
#         logger.error(f"Ошибка получения OAuth‑токена: {e}")
#         return None

# def chat_with_gigachat(token: str, prompt: str) -> str:
#     url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
#     headers = {
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "Authorization": f"Bearer {token}"
#     }
#     payload = {
#         "model": "GigaChat",
#         "messages": [{"role": "user", "content": prompt}]
#     }

#     try:
#         resp = requests.post(url, headers=headers, json=payload, timeout=10, verify=False)
#         resp.raise_for_status()
#         content = resp.json()["choices"][0]["message"]["content"]
#         logger.info(f"GigaChat ответ (raw): {content}")
#         return content
#     except Exception as e:
#         logger.error(f"Ошибка chat_with_gigachat: {e}")
#         return ""

# def get_recommendations(preferences, items):
#     """
#     Возвращает список ID трёх рекомендованных товаров.
#     Сначала пытаемся через GigaChat, затем — локальный фол‑бэк.
#     """
#     # 1) Готовим промпт, добавляем инструкцию "только JSON"
#     item_list_str = "\n".join(
#         f"- ID {item.id}: {item.name} (категория: {item.category}, цена: {item.price})"
#         for item in items
#     )
#     prompt = (
#         f"Покупатель заинтересован в категориях: {', '.join(preferences)}.\n"
#         f"Доступные товары:\n{item_list_str}\n"
#         "Ответь **только** JSON‑массивом трёх ID, например [1,2,3], без каких‑либо пояснений."
#     )
#     logger.info(f"Prompt для GigaChat:\n{prompt}")

#     # 2) Пытаемся получить от LLM
#     rec_ids = []
#     token = get_oauth_token()
#     if token:
#         raw = chat_with_gigachat(token, prompt)
#         # ищем JSON‑список в любом месте ответа
#         start = raw.find('[')
#         end = raw.rfind(']')
#         if start != -1 and end != -1:
#             snippet = raw[start:end+1]
#             try:
#                 parsed = json.loads(snippet)
#                 # поддерживаем оба формата: [3,5,7] или [{ "id":3 },…]
#                 if parsed and isinstance(parsed, list):
#                     if isinstance(parsed[0], dict) and 'id' in parsed[0]:
#                         rec_ids = [int(d['id']) for d in parsed]
#                     else:
#                         rec_ids = [int(x) for x in parsed]
#                     logger.info(f"Распознанный rec_ids от LLM: {rec_ids}")
#             except Exception as e:
#                 logger.error(f"Не удалось распарсить JSON из LLM: {e}")
#         else:
#             logger.error("В ответе LLM не найден JSON‑массив")

#     # 3) Локальный фол‑бэк, если LLM не дала трёх ID
#     # if not isinstance(rec_ids, list) or len(rec_ids) < 3:
#     #     logger.info("Используем локальный фол‑бэк")
#     #     filtered = [item for item in items if item.category in preferences] or items.copy()
#     #     filtered.sort(key=lambda x: x.price)
#     #     rec_ids = [item.id for item in filtered[:3]]
#     #     logger.info(f"Локальный rec_ids: {rec_ids}")

#     return rec_ids
