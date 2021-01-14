import argparse
import sys
import json
from .extraction.user import User
from .extraction.saved_users import UserDB
from .extraction.database import Database

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--numUsers', type=int, default=50, help="Number of users in the environment")
    parser.add_argument('--numDays', type=int, default=21, help="Number of days the test is conducted")
    parser.add_argument('--usersInDay', type=int, default=10, help="Number of active users in each day")

    return parser


def main(argv=None):
    """
    :desc: Entry point method
    """
    if argv is None:
        argv = sys.argv

    try:
        parser = create_parser()
        args = parser.parse_args(argv[1:])

        MY_PASS = json.loads(open('../../secretfiles.json', 'r').read())['web']['user_pw']
        Database.initialize(database='chainedSCT', user='i-sip_iot', password=MY_PASS, host='localhost')

        # user = User('patriciarobinson@gmail.com', 'Samantha', 'Gallegos', 66048763)
        # UserDB.users_submission(args)

        print(args.numUsers)

        # User.fetch_data()
        User.fetch_ids()


    except KeyboardInterrupt:
        print('\n Please run command --> [getTweets --h] to receive help the commands you can search')

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))