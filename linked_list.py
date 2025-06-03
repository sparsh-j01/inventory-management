from merge_sort import merge_sort
from binary_search import binary_search_by_id

class ProductNode:
    def __init__(self, product_id, name, quantity):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.next = None

class Inventory:
    def __init__(self):
        self.head = None

    def add_product(self, product_id, name, quantity):
        new_node = ProductNode(product_id, name, quantity)
        new_node.next = self.head
        self.head = new_node

    def remove_product(self, product_id):
        curr = self.head
        prev = None
        while curr:
            if curr.product_id == product_id:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                return True
            prev = curr
            curr = curr.next
        return False

    def get_all(self):
        result = []
        curr = self.head
        while curr:
            result.append({
                "product_id": curr.product_id,
                "name": curr.name,
                "quantity": curr.quantity
            })
            curr = curr.next
        return result

    def to_list(self):
        lst = []
        curr = self.head
        while curr:
            lst.append(curr)
            curr = curr.next
        return lst

    def sort_by_quantity(self):
        nodes = merge_sort(self.to_list(), key=lambda x: x.quantity if x.quantity is not None else 0)
        self.head = None
        for product in reversed(nodes):
            product.next = self.head
            self.head = product

    def search_by_id(self, product_id):
        return binary_search_by_id(self.to_list(), product_id)

    def search_by_name(self, name):
        curr = self.head
        while curr:
            if curr.name.lower() == name.lower():
                return curr
            curr = curr.next
        return None
