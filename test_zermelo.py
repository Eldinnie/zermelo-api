import dataclasses
import logging
from datetime import datetime, timezone, timedelta
from pprint import pprint

import requests_cache
from requests_cache import CachedSession

session = CachedSession(
    'demo_cache',
    use_cache_dir=True,                 # Save files in the default user cache dir
    cache_control=True,                 # Use Cache-Control headers for expiration, if available
    expire_after=timedelta(minutes=10), # Otherwise expire responses after one day
    allowable_methods=['GET'],          # Cache POST requests to avoid sending the same data twice
    allowable_codes=[200, 400],         # Cache 400 responses as a solemn reminder of your failures
    match_headers=True,                 # Match all request headers
    stale_if_error=True,                # In case of request errors, use stale cache data if possible
)

requests_cache.install_cache('demo_cache')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


from zermelo import Client, Appointment

c = Client("ggh", "8g7u81uemhinp329075oi94sl4", utc_offset=2)
sisy = c.get_school_in_school_year(2021)["schoolInSchoolYear"]
appointments = c.get_appointments(user=["gl"], schoolInSchoolYear=sisy, start=datetime(2021, 9, 14, 8), end=datetime(2021, 9, 14, 16), fields=["id", "startTimeSlot", "endTimeSlot", "subjects", "teachers", "locations", "valid", "base", "cancelled", "cancelledReason", "changeDescription", "groups", "appointmentInstance"])
print(len(appointments))
data = {}

for x in range(1,9):
    data[x] = {}

for a in appointments:
    data[a.startTimeSlot][a.appointmentInstance] = {}
    if a.base:
        data[a.startTimeSlot][a.appointmentInstance]["base"] = a
    if a.valid:
        data[a.startTimeSlot][a.appointmentInstance]["valid"] = a
    else:
        data[a.startTimeSlot][a.appointmentInstance]["rest"] = a

for x in range(1,9):
    print(x)
    for id, appointments in data[x].items():
        if a := appointments.get("base"):
            print(f"b  {', '.join(a.groups)} {', '.join(a.subjects)} ({', '.join(a.teachers)}) {', '.join(a.locations)} - {a.changeDescription}")
        if a := appointments.get("valid"):
            if a == appointments.get("base"): continue
            print(f"v  {', '.join(a.groups)} {', '.join(a.subjects)} ({', '.join(a.teachers)}) {', '.join(a.locations)} - {a.changeDescription}")
        if a := appointments.get("rest"):
            print(f"r  {', '.join(a.groups)} {', '.join(a.subjects)} ({', '.join(a.teachers)}) {', '.join(a.locations)} - {a.changeDescription}")