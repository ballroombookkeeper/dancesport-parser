from dataclasses import dataclass
from datetime import date

@dataclass
class Competition:
    id: str
    name: str
    date: date
