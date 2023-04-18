from ig.user import User
from ig.fnc import conn_restful_user_media
from ig.file import ImageFileSaveQueue
import argparse
import time

def main(args):
    ImageFileSaveQueue.get_instance().start()
    user = User(username=args.username, password=args.pwd, user_agent=args.user_agent)
    try:
        for i, target in enumerate(args.target):
            print("target", target)
            conn_restful_user_media(user=user, target_username="".join(target), sleep=args.sleep, have_next=not(len(args.target)-1 == i))
            time.sleep(5)
    except ValueError as e:
        print(f"Unknow Error: Please change your account whether Instagram soft locked. ({e})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download target user all post")
    parser.add_argument("--username", type=str, required=True, help="Instagram Username")
    parser.add_argument("--pwd", type=str, required=True, help="Instagram Password")
    parser.add_argument("--target", type=list, nargs="+", required=True, help="Target Instagram post short code")
    parser.add_argument("--output", type=str, help="Output Directory")
    parser.add_argument("--sleep", type=int, default=0, help="Sleep time for each request")
    parser.add_argument("--user_agent", type=str, required=True, help="Please enter your common User Agent")
    parser.add_argument("--cache_login", type=int, default=-1, help="create the .cache folder for reduce the login times")


    args = parser.parse_args()
    main(args)