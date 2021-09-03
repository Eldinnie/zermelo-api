from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Announcement:
    id: int
    start: int
    end: int
    title: str
    text: str
    branchesOfSchools: List[int]

    def __post_init__(self):
        self.start = datetime.utcfromtimestamp(self.start)
        self.end = datetime.utcfromtimestamp(self.end)