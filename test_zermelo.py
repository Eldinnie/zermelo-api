import dataclasses
import logging
from pprint import pprint

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


from zermelo import Client

c = Client("ggh", "8g7u81uemhinp329075oi94sl4")
sisy = c.get_school_in_school_year(2021)["schoolInSchoolYear"]
r = c.get_users(code=["vb", "ts", "su", "gp"], fields=["code", "displayName"])

pprint(r)