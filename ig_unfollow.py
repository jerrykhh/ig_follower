import argparse

from ig.user import User
from ig.fnc import use_unfollow

def main(args):
    user = User(username=args.username, password=args.pwd, user_agent=args.user_agent)
    use_unfollow(user=user, data_file=args.data, log_path=args.log)
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ig_follower: CSV UnFollow (using CSV)")
    parser.add_argument("--username", type=str, required=True, help="Instagram Username")
    parser.add_argument("--pwd", type=str, required=True, help="Instagram Password")
    parser.add_argument("--user_agent", type=str, required=True, help="Please enter your common User Agent")
    parser.add_argument("--data", type=str, required=True, help="Please enter the path of your datafile")
    parser.add_argument("--sleep", type=float, default=8*60, help="Please enter the sleep time for each follow request to avoid the account banned (sec per request), default is 8*60 sec per request")
    parser.add_argument("--log", type=str, default=None, help="Please enter the logging path for insert the logging")
    args = parser.parse_args()
    
    main(args)