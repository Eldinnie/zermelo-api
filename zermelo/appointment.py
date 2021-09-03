from dataclasses import dataclass
from datetime import datetime
from typing import List, Union

from zermelo import User


@dataclass
class Appointment:
    id: int
    appointmentInstance: int = None
    start: Union[int, datetime] = None
    end: Union[int, datetime] = None
    startTimeSlot: int = None
    startTimeSlotName: str = None
    endTimeSlot: int = None
    endTimeSlotName: str = None
    subjects: str = None
    branch: str = None
    type: str = None
    groupsInDepartments: List[int] = None
    locationsOfBranch: List[int] = None
    locations: List[int] = None
    modified: bool = None
    moved: bool = None
    optional: bool = None
    valid: bool = None
    cancelled: bool = None
    cancelledReason: str = None  # ['students' or 'teachers' or 'changedPlanning'],
    teacherChanged: bool = None
    groupChanged: bool = None
    locationChanged: bool = None
    timeChanged: bool = None
    created: Union[int, datetime] = None
    hidden: bool = None
    commonSchedule: bool = None
    ignoreSubstitutions: bool = None
    changeDescription: str = None
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
    teachers: List[User] = None
    onlineTeachers: List[User] = None
    students: list[User] = None
    branchOfSchool: str = None
    groups: List[str] = None

    def __post_init__(self):
        if self.start:
            self.start = datetime.utcfromtimestamp(self.start)
        if self.end:
            self.end = datetime.utcfromtimestamp(self.end)
        if self.created:
            self.created = datetime.utcfromtimestamp(self.created)
        if self.lastModified:
            self.lastModified = datetime.utcfromtimestamp(self.lastModified)
        if self.appointmentLastModified:
            self.appointmentLastModified = datetime.utcfromtimestamp(self.appointmentLastModified)