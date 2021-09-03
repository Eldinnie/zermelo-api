import dataclasses
import logging
from datetime import datetime
from pprint import pprint

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


from zermelo import Client

c = Client("ggh", "8g7u81uemhinp329075oi94sl4")
sisy = c.get_school_in_school_year(2021)["schoolInSchoolYear"]
lokalen = c.get_location_of_branches(schoolInSchoolYear=sisy)
lok = [lok for lok in lokalen if lok.name=="306" or lok.name=="308"]
users = c.get_users(code=["ts", "gp"])
r = c.get_appointments(start=datetime(2021, 8, 30, 8), end=datetime(2021, 8, 30, 16), schoolInSchoolYear=sisy, user=users)

pprint(r)