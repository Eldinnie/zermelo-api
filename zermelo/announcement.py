from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Any, Union


@dataclass
class Announcement:
    id: int
    start: Union[int, datetime]
    end: Union[int, datetime]
    title: str
    text: str
    branchesOfSchools: List[int]
    client: Any = None

    def __post_init__(self):
        self.start = datetime.fromtimestamp(self.start, self.client.utc_offset)
        self.end = datetime.fromtimestamp(self.end, self.client.utc_offset)