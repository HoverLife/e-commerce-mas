import os
from dotenv import load_dotenv

load_dotenv()  # загружаем настройки из .env
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from environment.simulator import Simulator
# импорт для мониторинга
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from fastapi.responses import FileResponse

app = FastAPI()

# Prometheus метрики
REQUEST_COUNT = Counter(
    'simulate_requests_total', 'Количество запросов к /simulate', ['method']
)
REQUEST_LATENCY = Histogram(
    'simulate_request_latency_seconds', 'Время обработки /simulate'
)

@app.get("/simulate")
async def simulate_sessions(count: int = 1):
    """
    Эндпоинт для запуска симуляции.
    Параметр count задаёт количество сессий.
    Возвращает рекомендации и CTR.
    """
    REQUEST_COUNT.labels(method='GET').inc()
    with REQUEST_LATENCY.time():
        simulator = Simulator()
        recommendations, ctr = simulator.simulate(count)

    # Формируем JSON-ответ
    return {"recommendations": [
        {"id": item.id, "name": item.name, "category": item.category, "price": item.price}
        for item in recommendations
    ], "ctr": ctr}

# Эндпоинт для метрик Prometheus
@app.get("/metrics")
async def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

# Монтируем статические файлы React
# Обслуживаем статические файлы React по префиксу /static
app.mount(
    "/static",
    StaticFiles(directory="frontend/build/static"),
    name="static"
)

# Корневой маршрут отдает index.html
from fastapi.responses import FileResponse

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse("frontend/build/index.html")