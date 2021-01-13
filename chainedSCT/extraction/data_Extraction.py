from .user import User
from datetime import datetime
import random

class UsersDataExtraction:

    def random_user_location(self):
        users_ids = User.fetch_ids()
        location_ = {'user_id': None, 'date_local': None, 'time_local': None, 'X': None, 'Y': None}
        now_date = datetime.now().date()
        now_time = datetime.now().time()
        date_local = now_date.strftime('%d/%b/%Y')
        time_local = now_time.strftime('%H:%M:%S')
        x_pos = random.uniform(0.0, 20.0)
        y_pos = random.uniform(0.0, 10.0)
        step_size = 0.5
        num_steps = random.randint(20, 60)
        for i in range(num_steps):
