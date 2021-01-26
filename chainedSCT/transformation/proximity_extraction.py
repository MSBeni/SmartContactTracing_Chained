from .proximity import Proximity
from ..extraction.user import User
from ..extraction.locations import Location
import numpy as np


class ProximityCALC:

    @staticmethod
    def prox_calc(argument_handler):
        unique_contact_dates = set(Location.fetch_loc_dates()[0])
        unique_contact_dates = list(unique_contact_dates)
        user_ids = User.load_all_ids_from_db()
        user_ids = user_ids[0]
        # unique_users_in_this_date = set(Location.fetch_proximity_ids_by_date(unique_contact_dates[0][0])[0])
        # print(set(unique_users_in_this_date[0]))
        Proximity.create_proximity_table()
        for date in unique_contact_dates:
            unique_users_in_this_date = set(Location.fetch_proximity_ids_by_date(date)[0])
            unique_users_in_this_date = list(unique_users_in_this_date)
            for user in unique_users_in_this_date:
                user_locations_data = set(Location.fetch_proximity_loc_by_date_id(date, user)[0])
                user_locations_data = list(user_locations_data)

                for other_users in unique_users_in_this_date:
                    if user != other_users:
                        other_user_locations_data = set(Location.fetch_proximity_loc_by_date_id(date, other_users)[0])
                        other_user_locations_data = list(other_user_locations_data)
                        for pos in user_locations_data:
                            for pos_other in other_user_locations_data:
                                distance = np.sqrt(np.power(float(pos[0]) - float(pos_other[0]), 2) +
                                                   np.power(float(pos[1]) - float(pos_other[1]), 2))

                                if distance < argument_handler.immediate:
                                    proximity = 'immediate'
                                elif argument_handler.immediate < distance < argument_handler.near:
                                    proximity = 'near'
                                else:
                                    proximity = 'far'

                                # print(date, user, other_users, distance, proximity)
                                proximity = Proximity(date, user[0], other_users[0], distance, proximity)
                                proximity.save_proximity_to_db()









