from .locations import Location
from .user import User
from datetime import datetime, timedelta
import random


class UsersDataExtraction:
    # def __init__(self, step_size=0.5):
    #     self.step_size = step_size

    @staticmethod
    def random_users():
        """
        based on the number of the active users in each day, randomly select user ids from user table
        :param argument_handler: imported arguments
        :return: list of the active user ids
        """
        ids_lst = User.load_all_ids_from_db()

        selected_users = list()
        users_In_Day = random.randint(10, len(ids_lst[0])-1)
        for i in range(users_In_Day):
            idx = random.randint(0, len(ids_lst[0])-1)
            selected_users.append(ids_lst[0][idx][0])

        return selected_users

    @classmethod
    def random_user_location(cls, step_size=0.5):
        """
        create locations based on defined step size and number of steps in the environment for each user
        :return: list of the positions' tuples
        """
        positions = list()
        x_pos = random.uniform(0.0, 20.0)
        y_pos = random.uniform(0.0, 10.0)
        positions.append((x_pos, y_pos))
        num_steps = random.randint(20, 50)
        while num_steps > 0:
            new_x_pos = x_pos + random.choice([-1, 1]) * step_size
            new_y_pos = y_pos + random.choice([-1, 1]) * step_size
            if (0.0 <= new_x_pos <= 20.0) and (0.0 <= new_y_pos <= 10.0):
                positions.append((new_x_pos, new_y_pos))
                num_steps -= 1

        return positions

    @classmethod
    def save_location_to_db(cls, argument_handler):
        """
        create data specifically for all the active users and save timestamped data containing the user's locations to
        database
        :param argument_handler: imported arguments
        :return:
        """
        # location_ = {'user_id': None, 'date_local': None, 'time_local': None, 'X': None, 'Y': None}
        selected_users = cls.random_users()
        xy_locations = cls.random_user_location()
        date_local = (datetime.today() - timedelta(days=1)).date()
        time_local = (datetime.now() - timedelta(seconds=1)).time()
        location_ = Location(selected_users[0], date_local, time_local, xy_locations[0][0], xy_locations[0][1])
        location_.create_locations_table()

        for user in selected_users:
            for j in range(argument_handler.numDays):
                date_local = (datetime.today() - timedelta(days=1)).date()
                xy_locations = cls.random_user_location()
                for i in range(len(xy_locations)):
                    time_local = (datetime.now() - timedelta(seconds=5)).time()
                    print(str(user), str(date_local), str(time_local), str(xy_locations[i][0]), str(xy_locations[i][1]))
                    location_ = Location(user, date_local, time_local, xy_locations[i][0], xy_locations[i][1])

                    location_.save_loc_to_db()

