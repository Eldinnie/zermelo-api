import dataclasses
import logging
from datetime import datetime, timezone, timedelta
from pprint import pprint

import requests_cache
from requests_cache import CachedSession

session = CachedSession(
    'demo_cache',
    use_cache_dir=True,                # Save files in the default user cache dir
    cache_control=True,                # Use Cache-Control headers for expiration, if available
    expire_after=timedelta(minutes=10),    # Otherwise expire responses after one day
    allowable_methods=['GET'], # Cache POST requests to avoid sending the same data twice
    allowable_codes=[200, 400],        # Cache 400 responses as a solemn reminder of your failures
    match_headers=True,                # Match all request headers
    stale_if_error=True,               # In case of request errors, use stale cache data if possible
)

requests_cache.install_cache('demo_cache')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


from zermelo import Client

c = Client("ggh", "8g7u81uemhinp329075oi94sl4", utc_offset=2)
sisy = c.get_school_in_school_year(2021)["schoolInSchoolYear"]
lok = c.get_location_of_branches(schoolInSchoolYear=sisy)
lok = [l for l in lok if l.name.startswith("b")]
# print(lok)
base = c.get_appointments(schoolInSchoolYear=sisy, start=datetime(2021, 9, 9, 8), end=datetime(2021, 9, 9, 16), base=True, valid=False)
print(len(base))
changes = c.get_appointments(appointmentInstance=[x.appointmentInstance for x in base], valid=True)
change_dict = {}
for x in changes:
    print(x.moved)
    change_dict.setdefault(x.startTimeSlot, {}).setdefault(x.appointmentInstance, x)

base_dict = {}
for x in base:
    base_dict.setdefault(x.appointmentInstance, x)


for time_slot in range(1,9):
    data = change_dict[time_slot]
    for id, appointment in data.items():
        if appointment.cancelled:
            print(f'{time_slot} - {", ".join(appointment.groups):8s} {", ".join(appointment.subjects):4s} {", ".join(appointment.teachers):15s} {", ".join(appointment.locations):10s} ---> {appointment.changeDescription}')
        else:
            base = base_dict[id]
            print(
                f'{time_slot} - {", ".join(base.groups):8s} {", ".join(base.subjects):4s} {", ".join(base.teachers):15s} {", ".join(base.locations):10s} ---> {", ".join(appointment.groups):8s} {", ".join(appointment.subjects):4s} {", ".join(appointment.teachers):15s} {", ".join(appointment.locations):10s} - {appointment.changeDescription}')
# for x in range(1,9 ):
#     for id, app in changes.setdefault(x, {}).items():
#         if changes[x][id].cancelled:
#             print(f'{x} - {", ".join(base[id].groups):8s} {", ".join(base[id].subjects):4s} {", ".join(base[id].teachers):15s} {", ".join(base[id].locations):10s} ---> {changes[x][id].changeDescription}')
#         else:
#             print(f'{x} - {", ".join(base[id].groups):8s} {", ".join(base[id].subjects):4s} {", ".join(base[id].teachers):15s} {", ".join(base[id].locations):10s} ---> {", ".join(changes[x][id].groups):10s} {", ".join(changes[x][id].subjects):10s} {", ".join(changes[x][id].teachers):10s} {", ".join(changes[x][id].locations):10s} - {changes[x][id].changeDescription}')
# #
#
# # r2.sort(key=lambda x: x.startTimeSlot)
#
#
# # for x in r2:
# #     print(f'{", ".join(x.groups)} {", ".join(x.subjects)} ({", ".join(x.teachers)}) {", ".join(x.locations)}')
# # # Appointment(id=3529, appointmentInstance=2284, start=datetime.datetime(2021, 9, 6, 8, 30, tzinfo=datetime.timezone(datetime.timedelta(seconds=7200))), end=datetime.datetime(2021, 9, 6, 9, 20, tzinfo=datetime.timezone(datetime.timedelta(seconds=7200))), startTimeSlot=1, startTimeSlotName='u1', endTimeSlot=1, endTimeSlotName='u1', subjects=['na'], branch='ggh', type='lesson', groupsInDepartments=[103], locationsOfBranch=[87], locations=['306'], modified=False, moved=False, optional=None, valid=False, cancelled=False, cancelledReason=None, teacherChanged=None, groupChanged=None, locationChanged=None, timeChanged=None, created=datetime.datetime(2021, 9, 5, 7, 30, 48, tzinfo=datetime.timezone(datetime.timedelta(seconds=7200))), hidden=False, commonSchedule=None, ignoreSubstitutions=None, changeDescription='', schedulerRemark=None, expectedStudentCount=None, expectedStudentCountOnline=None, content=None, capacity=None, new=False, choosableInDepartments=None, choosableInDepartmentCodes=None, alternativeSubject=None, onlineStudents=None, remark='', capacityManually=None, teachingTimeManually=None, teachingTime=None, availableSpace=None, udmUUID=None, lastModified=datetime.datetime(2021, 9, 5, 18, 38, 38, tzinfo=datetime.timezone(datetime.timedelta(seconds=7200))), appointmentLastModified=None, subject=None, teachers=['ts'], onlineTeachers=None, students=None, branchOfSchool=51, groups=['2c'], client=<zermelo.client.Client object at 0x0000023CA37CE940>),