from .proximity import Proximity
from ..extraction.user import User
from ..extraction.locations import Location
from ..extraction.database import CursorFromConnectionPool

class ProximityCALC:

    @staticmethod
    def prox_calc():
        unique_contact_dates = set(Location.fetch_loc_dates()[0])
        unique_contact_dates = list(unique_contact_dates)
        print(unique_contact_dates[0][0])
        user_ids = User.load_all_ids_from_db()
        user_ids = user_ids[0]
        print(user_ids[0][0])
        unique_users_in_this_date = set(Location.fetch_proximity_ids_by_date(unique_contact_dates[0][0])[0])
        print(unique_users_in_this_date)

        # unique_users_in_this_date = set(Location.fetch_proximity_loc_by_date_id(unique_contact_dates[0], user_ids[0])[0])
        unique_users_in_this_date = Location.fetch_proximity_loc_by_date_id(unique_contact_dates[0][0], user_ids[0][0])
        print(set(unique_users_in_this_date[0]))

        for date in unique_contact_dates:
            unique_users_in_this_date = set(Location.fetch_proximity_ids_by_date(date)[0])
            unique_users_in_this_date = list(unique_users_in_this_date)
            # for user in unique_users_in_this_date:
            #     user_los_data = Location.fetch_proximity_loc_by_date_id(date, user)[0]
            #     for other_users in unique_users_in_this_date:
            #         if user != other_users:








