from .authentication_IUP import AuthorizedUsers
import json

authorized_users = json.loads(open('../../../authorized_users.json', 'r').read())

num_of_authorized_users = len(authorized_users.keys())