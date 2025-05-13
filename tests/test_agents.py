import pytest
from agents.buyer_agent import buyer_agent

@pytest.mark.asyncio
async def test_buyer_agent():
    # если есть список товаров
    items = [{'id':1},{'id':2}]
    res = await buyer_agent(['electronics'], items)
    assert res == 1
    # если пусто
    res2 = await buyer_agent(['books'], [])
    assert res2 == -1