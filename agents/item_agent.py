class ItemAgent:
    """
    Агент-товар с идентификатором, названием, категорией и ценой.
    """
    def __init__(self, item_id, name, category, price):
        self.id = item_id
        self.name = name
        self.category = category
        self.price = price

    def __repr__(self):
        return (f"ItemAgent(id={self.id}, name={self.name}, "
                f"category={self.category}, price={self.price})")
