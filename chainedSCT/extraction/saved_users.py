from faker import Faker
from .user import User


class UserDB:
    __user_dict = {'ID': None,
                   'First_Name': None,
                   'Last_Name': None,
                   'Email': None}

    @staticmethod
    def users_submission(argument_handler):
        Faker.seed(0)
        fake = Faker()
        __users_lst = list()
        for _ in range(argument_handler.numUsers):
            user_info = __user_dict = {'ID': fake.ean(length=8),
                                       'First_Name': fake.first_name(),
                                       'Last_Name': fake.last_name(),
                                       'Email': fake.email()}

            __users_lst.append(user_info)

        user = User(__users_lst[1]['Email'], __users_lst[1]['First_Name'], __users_lst[1]['Last_Name'],
                    __users_lst[1]['ID'])
        user.create_users_table()
        for i in range(2, len(__users_lst)):
            user = User(__users_lst[i]['Email'], __users_lst[i]['First_Name'], __users_lst[i]['Last_Name'],
                        __users_lst[i]['ID'])

            user.save_to_db()



# Faker.seed(0)
# fake = Faker()
#
# users_lst = []
# users_dict = {'ID': None,
#               'First_Name': 'first_name',
#               'Last_Name': 'last_name',
#               'Email': 'email',
#               'Address': 'address'}
#
# for _ in range(50):
#     # users_json = fake.json(data_columns={'ID': 'pyint', 'Details': {'First_Name': 'first_name',
#     #                                                                 'Last_Name': 'last_name', 'Email': 'email',
#     #                                                                 'Address': 'address'}}, num_rows=1)
#     user = users_dict = {'ID': fake.ean(length=8),
#                          'First_Name': fake.first_name(),
#                          'Last_Name': fake.last_name(),
#                          'Email': fake.email(),
#                          'Address': fake.address()}
#
#     users_lst.append(user)
#
# print(users_lst)
# for i in range(50):
#     print(users_lst[i])
