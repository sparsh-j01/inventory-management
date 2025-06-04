from collections import deque

class OrderQueue:
    def __init__(self):
        self.queue = deque()

    def add_order(self, order_id):
        self.queue.append(order_id)

    def process_order(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def get_all(self):
        return list(self.queue)