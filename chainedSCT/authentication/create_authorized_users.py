from .authentication_IUP import AuthorizedUsers
import json


class AuthUser:

    authorized_users = json.loads(open('../../authorized_users.json', 'r').read())

    @classmethod
    def save_auth_user(cls):

        authorized_users_keys = cls.authorized_users.keys()
        AuthorizedUsers.create_authcheck_table()

        for auth_user in authorized_users_keys:
            auth_user_ = AuthorizedUsers(cls.authorized_users[auth_user]['user_id'],
                                         cls.authorized_users[auth_user]['user_name'],
                                         cls. authorized_users[auth_user]['user_pw'])

            auth_user_.save_authorized_users_to_db()

        return AuthorizedUsers.fetch_authorized_id()
