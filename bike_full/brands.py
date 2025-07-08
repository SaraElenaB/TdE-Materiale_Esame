import datetime
from datetime import date, time
from dataclasses import dataclass


@dataclass
class Brand:
    brand_id: int
    brand_name: str

    def __hash__(self):
        return hash(self.brand_id)

    def __eq__(self, other):
        return self.brand_id == other.brand_id

    def __str__(self):
        return f"{self.brand_id}"
