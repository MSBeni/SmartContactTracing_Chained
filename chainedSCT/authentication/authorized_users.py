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
        # print(reg_credential)
        # print(reg_credential['id'])
        # print(AuthorizedUsers.fetch_authorized_id())
        # print(AuthorizedUsers.password_check_for_id(reg_credential['id']))
        # print(AuthorizedUsers.password_check_for_id(reg_credential['id']))
        # print(reg_credential['password'] == AuthorizedUsers.password_check_for_id(reg_credential['id'])[0])
        # print(int(reg_credential['id']), reg_credential['password'])
        if int(reg_credential['id']) not in AuthorizedUsers.fetch_authorized_id():
            return {"message": "You are not specified as an authorized user"}, 400

        elif reg_credential['password'] == AuthorizedUsers.password_check_for_id(reg_credential['id'])[0]:
            accepted_user = AuthAcceptedUsers(int(reg_credential['id']), reg_credential['password'])
            accepted_user.save_accepted_auth_to_db()
            return {"message": "User {} is admitted in IUP Managers".format(reg_credential['id'])}, 201

        return {"message": "User {} is noe allowed to have this access".format(reg_credential['id'])}, 400

