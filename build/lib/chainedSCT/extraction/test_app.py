from .database import Database
from .user import User
import json
# from Postgresql.postgre_Small_project.database import Database

MY_PASS = json.loads(open('../../../../secretfiles.json', 'r').read())['web']['user_pw']

Database.initialize(database='chainedSCT', user='i-sip_iot', password=MY_PASS, host='localhost')

user = User('frank@Uniofcode.me', 'Frank', 'Raykard')
user.create_users_table()
user.save_to_db()
user.fetch_data()

user = User.load_from_db_by_email('jose@schoolofcode.me')
print(user)
