from werkzeug.security import safe_str_cmp
from .authentication_IUP import AuthAcceptedUsers


def authenticate(id_, password):
    # print(AuthAcceptedUsers.fetch_All_authorized_IUP(93877848))
    # print(AuthAcceptedUsers.get_auth_user_by_id(93877848))
    user = AuthAcceptedUsers.get_auth_user_by_id(int(id_))
    print("user: ", user)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return AuthAcceptedUsers.get_auth_user_by_id(user_id)

