from flask_restful import Resource, reqparse
from .create_authorized_users import AuthUser
from .authentication_IUP import AuthorizedUsers
from .authentication_IUP import AuthAcceptedUsers


class UserCredentialCheck(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=str,
                        required=True,
                        help='The username field cannot be empty')

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='The password field cannot be empty')

    def post(self):
        AuthAcceptedUsers.create_iupmanagers_table()
        reg_credential = UserCredentialCheck.parser.parse_args()

        if reg_credential['id'] not in AuthUser:
            return {"message": "You are not specified as an authorized user"}, 400

        elif reg_credential['password'] == AuthorizedUsers.password_check_for_id(reg_credential['password']):
            accepted_user = AuthAcceptedUsers(reg_credential['id'], reg_credential['password'])
            accepted_user.save_accepted_auth_to_db()

        return {"message": "User {} is noe allowed to have this access".format(reg_credential['username'])}, 400

