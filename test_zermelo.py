import dataclasses
import logging
from datetime import datetime, timezone, timedelta
from pprint import pprint


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


from zermelo import Client

c = Client("ggh", "8g7u81uemhinp329075oi94sl4", utc_offset=2)
sisy = c.get_school_in_school_year(2021)["schoolInSchoolYear"]
r = c.get_appointments(schoolInSchoolYear=sisy, start=datetime(2021, 9, 6, 8), base=True, end=datetime(2021, 9, 6, 16), user=["vb"])


pprint(r)