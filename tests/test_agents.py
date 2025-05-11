import pytest
from agents.buyer_agent import BuyerAgent
from agents.item_agent import ItemAgent
from agents.marketplace_agent import MarketplaceAgent

def test_buyer_agent_preferences():
    buyer = BuyerAgent(["electronics", "books"])
    assert "electronics" in buyer.preferences

def test_item_agent_attributes():
    item = ItemAgent(1, "Test Item", "test_category", 100.0)
    assert item.id == 1
    assert item.name == "Test Item"
    assert item.category == "test_category"
    assert item.price == 100.0

def test_marketplace_recommendation_fallback():
    items = [
        ItemAgent(1, "A", "electronics", 50.0),
        ItemAgent(2, "B", "books", 30.0),
        ItemAgent(3, "C", "electronics", 20.0),
    ]
    marketplace = MarketplaceAgent(items)
    buyer = BuyerAgent(["electronics"])
    recs = marketplace.recommend(buyer)
    # Ожидаем сортировку по цене среди товаров категории electronics: ID 3, затем 1
    rec_ids = [item.id for item in recs]
    assert rec_ids == [3, 1]
