from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Union, Any

from zermelo import User


@dataclass
class Appointment:
    id: int
    startTimeSlot: int = None
    startTimeSlotName: str = None
    locations: List[int] = None
    subjects: str = None
    teachers: List[User] = None
    valid: bool = None
    cancelled: bool = None
    base: bool = None
    changeDescription: str = None
    appointmentInstance: int = None
    start: Union[int, datetime] = None
    end: Union[int, datetime] = None
    endTimeSlot: int = None
    endTimeSlotName: str = None
    branch: str = None
    type: str = None
    groupsInDepartments: List[int] = None
    locationsOfBranch: List[int] = None
    modified: bool = None
    moved: bool = None
    optional: bool = None
    cancelledReason: str = None  # ['students' or 'teachers' or 'changedPlanning'],
    teacherChanged: bool = None
    groupChanged: bool = None
    locationChanged: bool = None
    timeChanged: bool = None
    created: Union[int, datetime] = None
    hidden: bool = None
    commonSchedule: bool = None
    ignoreSubstitutions: bool = None
    schedulerRemark: str = None
    expectedStudentCount: int = None
    expectedStudentCountOnline: int = None
    content: str = None
    capacity: int = None
    new: bool = None
    choosableInDepartments: List[int] = None
    choosableInDepartmentCodes: List[str] = None
    alternativeSubject: str = None
    onlineStudents: List[str] = None
    remark: str = None
    capacityManually: bool = None
    teachingTimeManually: bool = None
    teachingTime: int = None
    availableSpace: int = None
    udmUUID: str = None
    lastModified: Union[int, datetime] = None
    appointmentLastModified: Union[int, datetime] = None
    subject: List[str] = None
    onlineTeachers: List[User] = None
    students: list[User] = None
    branchOfSchool: str = None
    groups: List[str] = None
    client: Any = None

    def __post_init__(self):
        if self.start:
            self.start = datetime.fromtimestamp(self.start, self.client.utc_offset)
        if self.end:
            self.end = datetime.fromtimestamp(self.end, self.client.utc_offset)
        if self.created:
            self.created = datetime.fromtimestamp(self.created, self.client.utc_offset)
        if self.lastModified:
            self.lastModified = datetime.fromtimestamp(self.lastModified, self.client.utc_offset)
        if self.appointmentLastModified:
            self.appointmentLastModified = datetime.fromtimestamp(self.appointmentLastModified, self.client.utc_offset)