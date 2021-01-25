import json
from .authentication_IUP import IUP


class InfectedUsersPool:

    infected_users = json.loads(open('../../IUP.json', 'r').read())

    @classmethod
    def save_auth_user(cls):

        infected_users_keys = cls.infected_users.keys()
        IUP.create_infection_table()

        for infected_user in infected_users_keys:
            infected_user_ = IUP(cls.infected_users[infected_user]['user_id'],
                                 cls.infected_users[infected_user]['date'])

            infected_user_.save_infected_users_to_db()

        return IUP.fetch_iup_data()
