from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Any, Union


@dataclass
class User:
    code: str
    displayName: str = None
    firstName: str = None
    prefix: str = None
    lastName: str = None
    email: str = None
    ldap: bool = None
    roles: List[str] = None
    admin: bool = None
    username: str = None
    userPrincipalName: str = None
    somUUID: str = None
    magisterUUID: str = None
    gender: str = None
    street: str = None
    city: str = None
    dateOfBirth: Union[int, datetime] = None
    userKind: str = None
    schoolInSchoolYears: List[int] = None
    studentSchoolInSchoolYears: List[int] = None
    employeeSchoolInSchoolYears: List[int] = None
    familyMemberSchoolInSchoolYears: List[int] = None
    subjectSelectionSchoolInSchoolYears: List[int] = None
    parentTeacherNightOfTeacherIds: List[int] = None
    isApplicationManager: bool = None
    archived: bool = None
    isStudent: bool = None
    isEmployee: bool = None
    isFamilyMember: bool = None
    houseNumber: str = None
    postalCode: str = None
    isSchoolScheduler: bool = None
    isSchoolLeader: bool = None
    isStudentAdministrator: bool = None
    isTeamLeader: bool = None
    isSectionLeader: bool = None
    isMentor: bool = None
    isParentTeacherNightScheduler: bool = None
    isDean: bool = None
    hasPassword: bool = None
    client: Any = None

    def __post_init__(self):
        if self.dateOfBirth:
            self.dateOfBirth = datetime.fromtimestamp(int(self.dateOfBirth), self.client.utc_offset)