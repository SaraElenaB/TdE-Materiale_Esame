from dataclasses import dataclass


@dataclass
class Stock:
    store_id: int
    product_id: int
    quantity: int

    def __hash__(self):
        return hash( (self.store_id, self.product_id ) )

    def __eq__(self, other):
        return (self.store_id, self.product_id) == (other.store_id , other.product_id)

    def __str__(self):
        return f"{self.store_id}"