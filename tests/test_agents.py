import pytest
from giga_integration.negotiation_protocol import build_negotiation_graph

@pytest.mark.asyncio
async def test_negotiation_protocol():
    graph = build_negotiation_graph()
    initial_state = {"messages": [], "sender": ""}
    final_state = await graph.run(initial_state)
    assert isinstance(final_state, dict)
    messages = final_state.get("messages", [])
    # Есть хотя бы одно сообщение от Buyer с предложением
    assert any(hasattr(msg, "content") and "offer" in msg.content.lower()
               for msg in messages)
    # Есть ответ Seller с «Deal» или «counteroffer»
    assert any(hasattr(msg, "content") and
               ("deal" in msg.content.lower() or "counteroffer" in msg.content.lower())
               for msg in messages)
