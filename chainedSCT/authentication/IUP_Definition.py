import json
from .authentication_IUP import IUP
from datetime import datetime, timedelta


class InfectedUsersPool:

    infected_users = json.loads(open('../../IUP.json', 'r').read())
    # print("infected_users: ", infected_users)

    @classmethod
    def save_infected_user(cls):

        infected_users_keys = cls.infected_users.keys()
        IUP.create_infection_table()

        for infected_user in infected_users_keys:
            date_ = datetime.strptime(cls.infected_users[infected_user]['date'], '%Y-%m-%d').date()
            infected_user_ = IUP(cls.infected_users[infected_user]['user_id'], date_)
            infected_user_.save_infected_users_to_db()

        return IUP.fetch_iup_data()
