from .user import User
from datetime import datetime
import random

class UsersDataExtraction:
    def __init__(self, step_size=0.5):
        self.step_size = step_size

    @staticmethod
    def random_users(argument_handler):
        """
        based on the number of the active users in each day, randomly select user ids from user table
        :param argument_handler: imported arguments
        :return: list of the active user ids
        """
        users_ids = User.fetch_ids()
        selected_users = list()
        for i in range(argument_handler.usersInDay):
            idx = random.randint(0, argument_handler.numUsers)
            selected_users.append(users_ids[idx][0])

        return selected_users

    def random_user_location(self):
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
            new_x_pos = x_pos + random.choice([-1, 1]) * self.step_size
            new_y_pos = y_pos + random.choice([-1, 1]) * self.step_size
            if (0.0 <= new_x_pos <= 20.0) and (0.0 <= new_y_pos <= 10.0):
                positions.append((new_x_pos, new_y_pos))
                num_steps -= 1

        return positions

    @classmethod
    def save_to_db(cls, argument_handler):
        selected_users = cls.random_users(argument_handler)
        for user in selected_users:
            for j in range(argument_handler.numDays):
                location_ = {'user_id': None, 'date_local': None, 'time_local': None, 'X': None, 'Y': None}
                now_date = datetime.now().date()
                now_time = datetime.now().time()
                date_local = now_date.strftime('%d/%b/%Y')
                time_local = now_time.strftime('%H:%M:%S')
