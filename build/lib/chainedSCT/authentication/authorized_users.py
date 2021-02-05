from flask_restful import Resource, reqparse
from .create_authorized_users import AuthUser
from .authentication_IUP import AuthorizedUsers
from .authentication_IUP import AuthAcceptedUsers


class UserCredentialCheck(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='The username field cannot be empty')

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='The password field cannot be empty')

    def post(self):
        # Reading the authorized users' information from the private file
        AuthUser.save_auth_user()
        AuthAcceptedUsers.create_iupmanagers_table()
        reg_credential = UserCredentialCheck.parser.parse_args()
        if reg_credential['username'] not in AuthorizedUsers.fetch_authorized_username():
            return {"message": "You are not specified as an authorized user"}, 400

        elif reg_credential['password'] == AuthorizedUsers.password_check_for_username(reg_credential['username'])[0]:
            accepted_user = AuthAcceptedUsers(AuthorizedUsers.id_check_for_username(reg_credential['username'])[0],
                                              reg_credential['username'], reg_credential['password'])
            accepted_user.save_accepted_auth_to_db()
            return {"message": "User {} is admitted in IUP Managers".format(reg_credential['username'])}, 201

        return {"message": "User {} is noe allowed to have this access".format(reg_credential['username'])}, 400

