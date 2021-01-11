import argparse
import sys
from .extraction.create_user import User

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

        user = User('jose@schoolofcode.me', 'Jose', 130)

        print(args.numUsers, user)


    except KeyboardInterrupt:
        print('\n Please run command --> [getTweets --h] to receive help the commands you can search')

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))