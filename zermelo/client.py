import dataclasses
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Union

import requests

from zermelo import Announcement, User, Location, Appointment


class Client:
    def __init__(self, school: str, api_key: str, utc_offset=None):
        self.logger = logging.getLogger("zermelo.Client")
        self.school = school
        self.api_key = api_key
        if utc_offset:
            self.utc_offset = timezone(timedelta(hours=utc_offset))
        else:
            self.utc_offset = timezone(timedelta(hours=0))

        self.params = {"access_token": self.api_key}
        self.base = f"https://{self.school}.zportal.nl:443/api/v3/"

    def get(self, url: str, params: dict, data: dict = None):
        self.logger.debug(f"requesting {url} - params: {params} - data: {data}")
        r: requests.Response = requests.get(url=url, params=params, data=data)
        self.logger.debug(f"status code: {r.status_code}")
        try:
            r.raise_for_status()
        except Exception as e:
            self.logger.error(e)
        return r.json()["response"]["data"]

    def get_announcements(self, current: bool = True, fields: List[str] = None, schoolInSchoolYear: int = None):
        self.logger.debug("get_announcements")
        url = f"{self.base}announcements"
        fields = fields or [x.name for x in dataclasses.fields(Announcement) if x.name != "client"]
        params = self.params | {"current": current, "fields": ",".join(fields)}
        if schoolInSchoolYear:
            params |= {"schoolInSchoolYear": schoolInSchoolYear}
        r = self.get(url, params)
        ret = [Announcement(**dat | {"client": self}) for dat in r]
        return ret

    def get_announcement(self, id: int, fields: List[str] = None, schoolInSchoolYear: int = None):
        self.logger.debug(f"get_announcement")
        url = f"{self.base}announcements/{id}"
        fields = fields or [x.name for x in dataclasses.fields(Announcement)]
        params = self.params | {"fields": ",".join(fields)}
        if schoolInSchoolYear:
            params |= {"schoolInSchoolYear": schoolInSchoolYear}
        r = self.get(url, params)
        ret = Announcement(**(r[0] | {"client": self}))
        return ret

    def get_users(self, code: List[str] = None, students: bool = False, family: bool = False, employees: bool = False,
                  fields: List[str] = None, schoolInSchoolYear: int = None):
        if not (students or family or employees) and not code:
            raise TypeError("must supply either one of the bools or specific codes")

        self.logger.debug(f"get_users")
        url = f"{self.base}users"
        fields = fields or [x.name for x in dataclasses.fields(User) if x.name != "client"]
        params = self.params | {"fields": ",".join(fields)}
        if schoolInSchoolYear:
            params |= {"schoolInSchoolYear": schoolInSchoolYear}
        if code:
            params |= {"code": ",".join(code)}
        else:
            params |= {"isStudent": students, "isFamilyMember": family, "isEmployee": employees}
        r = self.get(url, params)
        ret = [User(**dat | {"client": self}) for dat in r]
        return ret

    def get_user(self, code: str, fields: List[str] = None, schoolInSchoolYear: int = None):
        self.logger.debug(f"get_user")
        url = f"{self.base}users/{code}"
        fields = fields or [x.name for x in dataclasses.fields(User) if x.name != "client"]
        params = self.params | {"fields": ",".join(fields)}
        if schoolInSchoolYear:
            params |= {"schoolInSchoolYear": schoolInSchoolYear}
        r = self.get(url, params)
        ret = User(**r[0] | {"client": self})
        return ret

    def get_school_in_school_year(self, year: Union[str, int], fields: List[str] = []):
        self.logger.debug(f"get_school_in_school_year")
        url = f"{self.base}branchesofschools"
        params = self.params | {"schoolYear": year}
        if fields:
            params |= {"fields": ",".join(fields)}
        r = self.get(url, params)
        ret = r[0]
        return ret

    def get_location_of_branches(self, schoolInSchoolYear: int = None, branch: str = None, fields: List[str] = None):
        self.logger.debug(f"get_location_of_branches")
        url = f"{self.base}locationofbranches"
        fields = fields or [x.name for x in dataclasses.fields(Location) if x.name != "client"]
        params = self.params | {"fields": ",".join(fields)}
        if schoolInSchoolYear:
            params["schoolInSchoolYear"] = schoolInSchoolYear
        if branch:
            params["branch"] = branch
        r = self.get(url, params)
        ret = [Location(**dat | {"client": self}) for dat in r]
        return ret

    def get_appointments(self, start: Union[int, datetime] = None, end: Union[int, datetime] = None,
                         locations: List[Union[int, Location]] = None, user: List[Union[str, User]] = None, fields: List[str] = None,
                         schoolInSchoolYear: int = None, appointmentInstance: Union[List[int], int] = None, **kwargs):
        self.logger.debug(f"get_appointments")
        url = f"{self.base}appointments"
        params = {}
        params = params | self.params
        if appointmentInstance and type(appointmentInstance) == list:
            params["appointmentInstance"] = ",".join(str(a) for a in appointmentInstance)
        if start:
            params["start"] = type(start) == int and start or int(start.timestamp())
        if end:
            params["end"] = type(end) == int and end or int(end.timestamp())
        if locations:
            tmp = []
            for lok in locations:
                if type(lok) == int:
                    tmp.append(str(lok))
                elif type(lok) == Location:
                    tmp.append(str(lok.id))
                else:
                    raise TypeError("Locations must be a list of either zermelo.Locations or int")
            params["locationsOfBranch"] = ",".join(tmp)
        if user:
            tmp = []
            for us in user:
                if type(us) == str:
                    tmp.append(us)
                elif type(us) == User:
                    tmp.append(us.code)
                else:
                    raise TypeError("user must be a list of either zermelo.User or str")
            params["user"] = ",".join(tmp)
        if fields:
            params["fields"] = ",".join(fields)
        if schoolInSchoolYear:
            params["schoolInSchoolYear"] = schoolInSchoolYear
        params |= kwargs
        r = self.get(url, params)
        ret = [Appointment(**dat | {"client": self}) for dat in r]
        return ret
