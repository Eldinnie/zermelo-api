from dataclasses import dataclass
from typing import List


@dataclass
class Location:
    id: int
    name: str
    parentteachernightCapacity: int = None
    courseCapacity: int = None
    supportsConcurrentAppointments: bool = None
    branchOfSchool: int = None
    secondaryBranches: List[int] = None