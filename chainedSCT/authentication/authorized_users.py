from flask_restful import Resource, reqparse


class UserRegister(Resource):
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
        reg_credential = UserRegister.parser.parse_args()

        if User.get_user_by_username(reg_credential['username']):
            return {"message": "This Username already exists, please try another username"}, 400
        connection = sqlite3.connect('data.db')
        cur = connection.cursor()

        cur.execute("INSERT INTO users VALUES (NULL,?,?)", (reg_credential['username'], reg_credential['password']))

        connection.commit()
        connection.close()

        return {"message": "User {} is created successfully".format(reg_credential['username'])}, 201