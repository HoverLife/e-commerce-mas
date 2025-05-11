# giga_integration/negotiation_protocol.py
import os
import json
import uuid
import requests
import logging
import urllib3

# Отключаем предупреждения про self‑signed SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("negotiation_protocol")

def get_oauth_token():
    auth_token = os.getenv("GIGA_AUTH_HEADER")
    scope = os.getenv("GIGA_SCOPE")
    if not auth_token:
        logger.warning("GIGA_AUTH_HEADER не задан — пропускаем OAuth")
        return None

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
        "Authorization": f"Basic {auth_token}"
    }
    data = {"scope": scope}

    try:
        resp = requests.post(url, headers=headers, data=data, timeout=5, verify=False)
        resp.raise_for_status()
        token = resp.json().get("access_token")
        logger.info(f"Получен OAuth‑токен: {token[:10]}…")
        return token
    except Exception as e:
        logger.error(f"Ошибка получения OAuth‑токена: {e}")
        return None

def chat_with_gigachat(token: str, prompt: str) -> str:
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "model": "GigaChat",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10, verify=False)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        logger.info(f"GigaChat ответ (raw): {content}")
        return content
    except Exception as e:
        logger.error(f"Ошибка chat_with_gigachat: {e}")
        return ""

def get_recommendations(preferences, items):
    """
    Возвращает список ID трёх рекомендованных товаров.
    Сначала пытаемся через GigaChat, затем — локальный фол‑бэк.
    """
    # 1) Готовим промпт, добавляем инструкцию "только JSON"
    item_list_str = "\n".join(
        f"- ID {item.id}: {item.name} (категория: {item.category}, цена: {item.price})"
        for item in items
    )
    prompt = (
        f"Покупатель заинтересован в категориях: {', '.join(preferences)}.\n"
        f"Доступные товары:\n{item_list_str}\n"
        "Ответь **только** JSON‑массивом трёх ID, например [1,2,3], без каких‑либо пояснений."
    )
    logger.info(f"Prompt для GigaChat:\n{prompt}")

    # 2) Пытаемся получить от LLM
    rec_ids = []
    token = get_oauth_token()
    if token:
        raw = chat_with_gigachat(token, prompt)
        # ищем JSON‑список в любом месте ответа
        start = raw.find('[')
        end = raw.rfind(']')
        if start != -1 and end != -1:
            snippet = raw[start:end+1]
            try:
                parsed = json.loads(snippet)
                # поддерживаем оба формата: [3,5,7] или [{ "id":3 },…]
                if parsed and isinstance(parsed, list):
                    if isinstance(parsed[0], dict) and 'id' in parsed[0]:
                        rec_ids = [int(d['id']) for d in parsed]
                    else:
                        rec_ids = [int(x) for x in parsed]
                    logger.info(f"Распознанный rec_ids от LLM: {rec_ids}")
            except Exception as e:
                logger.error(f"Не удалось распарсить JSON из LLM: {e}")
        else:
            logger.error("В ответе LLM не найден JSON‑массив")

    # 3) Локальный фол‑бэк, если LLM не дала трёх ID
    # if not isinstance(rec_ids, list) or len(rec_ids) < 3:
    #     logger.info("Используем локальный фол‑бэк")
    #     filtered = [item for item in items if item.category in preferences] or items.copy()
    #     filtered.sort(key=lambda x: x.price)
    #     rec_ids = [item.id for item in filtered[:3]]
    #     logger.info(f"Локальный rec_ids: {rec_ids}")

    return rec_ids

class GigaChatNegotiator:
    """
    Обёртка для упрощённого общения с GigaChat:
    получает OAuth-токен один раз и отправляет промпты методом ask().
    """
    def __init__(self):
        self.token = get_oauth_token()

    def ask(self, prompt: str) -> str:
        if not self.token:
            # токен не получен — возвращаем пустую строку
            return ""
        return chat_with_gigachat(self.token, prompt)
    




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
