from .proximity import Proximity
from ..extraction.user import User
from ..extraction.locations import Location
from ..extraction.database import CursorFromConnectionPool

class ProximityCALC:

    @staticmethod
    def prox_calc():
        unique_contact_dates = set(Location.fetch_loc_dates()[0])
        unique_contact_dates = list(unique_contact_dates)

        user_ids = User.load_all_ids_from_db()
        user_ids = user_ids[0]
        # unique_users_in_this_date = set(Proximity.fetch_proximity_ids_by_date(unique_contact_dates[0])[0])
        # print(unique_users_in_this_date)
        for date in unique_contact_dates:
            unique_users_in_this_date = set(Location.fetch_proximity_ids_by_date(date)[0])







