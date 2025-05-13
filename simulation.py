import asyncio
from graph.graph import graph
from state.state import MessagesState

def main():
    prefs = input("Enter categories separated by space: ").split()
    state: MessagesState = {"messages": [], "current_item": None, "recommended_items": [], "final_price": 0.0, 'user_query': ' '.join(prefs)}
    out = asyncio.run(graph.invoke(state))
    print("Final state:", out)

if __name__ == "__main__":
    main()