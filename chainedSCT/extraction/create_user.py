

class User:
    def __init__(self, email, name, user_id):
        self.email = email
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return "<User {} >".format(self.email)

