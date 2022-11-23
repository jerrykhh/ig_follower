import argparse

from ig.user import User
from ig.fnc import use_follow

def main(args):
    user = User(username=args.username, password=args.pwd, user_agent=args.user_agent)
    use_follow(user=user, data_file=args.data, log_path=args.log)
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ig_follower: CSV Follow (using CSV)")
    parser.add_argument("--username", type=str, required=True, help="Instagram Username")
    parser.add_argument("--pwd", type=str, required=True, help="Instagram Password")
    parser.add_argument("--user_agent", type=str, required=True, help="Please enter your common User Agent")
    args = parser.parse_args()
    
    main(args)