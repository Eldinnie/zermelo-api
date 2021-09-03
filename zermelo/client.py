import dataclasses
import logging
from typing import List, Union

import requests

from zermelo import Announcement, User, Location


class Client:
    def __init__(self, school: str, api_key: str):
        self.logger = logging.getLogger("zermelo.Client")
        self.school = school
        self.api_key = api_key

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
        fields = fields or [x.name for x in dataclasses.fields(Announcement)]
        params = self.params | {"current": current, "fields": ",".join(fields)}
        if schoolInSchoolYear:
            params |= {"schoolInSchoolYear": schoolInSchoolYear}
        r = self.get(url, params)
        ret = [Announcement(**dat) for dat in r]
        return ret

    def get_announcement(self, id: int, fields: List[str] = None, schoolInSchoolYear: int = None):
        self.logger.debug(f"get_announcement")
        url = f"{self.base}announcements/{id}"
        fields = fields or [x.name for x in dataclasses.fields(Announcement)]
        params = self.params | {"fields": ",".join(fields)}
        if schoolInSchoolYear:
            params |= {"schoolInSchoolYear": schoolInSchoolYear}
        r = self.get(url, params)
        ret = Announcement(**r[0])
        return ret

    def get_users(self, code: List[str] = None, students:bool=False, family:bool=False, employees:bool=False, fields: List[str] = None, schoolInSchoolYear: int = None):
        if not (students or family or employees) and not code:
            raise TypeError("must supply either one of the bools or specific codes")

        self.logger.debug(f"get_users")
        url = f"{self.base}users"
        fields = fields or [x.name for x in dataclasses.fields(User)]
        params = self.params | {"fields": ",".join(fields)}
        if schoolInSchoolYear:
            params |= {"schoolInSchoolYear": schoolInSchoolYear}
        if code:
            params |= {"code": ",".join(code)}
        else:
            params |= {"isStudent": students, "isFamilyMember": family, "isEmployee": employees}
        r = self.get(url, params)
        ret = [User(**dat) for dat in r]
        return ret

    def get_user(self, code:str, fields: List[str] = None, schoolInSchoolYear: int = None):
        self.logger.debug(f"get_user")
        url = f"{self.base}users/{code}"
        fields = fields or [x.name for x in dataclasses.fields(User)]
        params = self.params | {"fields": ",".join(fields)}
        if schoolInSchoolYear:
            params |= {"schoolInSchoolYear": schoolInSchoolYear}
        r = self.get(url, params)
        ret = User(**r[0])
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
        fields = fields or [x.name for x in dataclasses.fields(Location)]
        params = self.params | {"fields": ",".join(fields)}
        if schoolInSchoolYear:
            params |= {"schoolInSchoolYear": schoolInSchoolYear}
        if branch:
            params |= {"branch": branch}
        r = self.get(url, params)
        ret = [Location(**dat) for dat in r]
        return ret