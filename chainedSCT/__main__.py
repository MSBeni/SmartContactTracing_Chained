import argparse
import sys
import json
from .extraction.user import User
from .extraction.saved_users import UserDB
from .extraction.database import Database

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--numUsers', type=int, help="Number of users in the environment")

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

        MY_PASS = json.loads(open('../../../../secretfiles.json', 'r').read())['web']['user_pw']
        Database.initialize(database='chainedSCT', user='i-sip_iot', password=MY_PASS, host='localhost')

        user = User('Samantha', 'Gallegos', 'patriciarobinson@gmail.com', 66048763)
        UserDB.users_submission(args.numUsers)

        print(args.numUsers)

        user.fetch_data()


    except KeyboardInterrupt:
        print('\n Please run command --> [getTweets --h] to receive help the commands you can search')

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))