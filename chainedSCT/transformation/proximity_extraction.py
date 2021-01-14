from .proximity import Proximity
from ..extraction.user import User
from ..extraction.locations import Location
from ..extraction.database import CursorFromConnectionPool

class ProximityCALC:

    @staticmethod
    def prox_calc():
        unique_contact_dates = set(Location.fetch_loc_dates()[0])


