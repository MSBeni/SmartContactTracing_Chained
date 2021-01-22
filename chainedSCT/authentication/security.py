from werkzeug.security import safe_str_cmp
from .authentication_IUP import AuthAcceptedUsers


def authenticate(id_, password):
    user = AuthAcceptedUsers.get_authenticated_user_by_id(int(id_))
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return AuthAcceptedUsers.get_authenticated_user_by_id(user_id)

