class Repository:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def get_all(self):
        return self.items

    def find_by_id(self, item_id):
        for item in self.items:
            if getattr(item, 'room_id', None) == item_id or getattr(item, 'user_id', None) == item_id or getattr(item, 'reservation_id', None) == item_id:
                return item
        return None
