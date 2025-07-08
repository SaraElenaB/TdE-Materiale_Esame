import datetime
from datetime import date, time
from dataclasses import dataclass


@dataclass
class Staff:
    staff_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    active: str
    store_id: int
    manager_id: int

    def __hash__(self):
        return hash(self.staff_id)

    def __eq__(self, other):
        return self.staff_id == other.staff_id

    def __str__(self):
        return f"{self.staff_id}"