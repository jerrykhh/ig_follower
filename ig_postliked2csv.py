from ig.user import User
from ig.fnc import conn_graphql_like_edge, conn_restful_like_edge
import argparse
import time

def main(args):
    user = User(username=args.username, password=args.pwd, user_agent=args.user_agent)
    cache_login =  True if (args.cache_login == 1) else False

    try:
        for i, target in enumerate(args.target):
            if args.output is None:
                conn_restful_like_edge(user=user, cache_login=cache_login ,short_code="".join(target), media_id=None)
            else:
                conn_restful_like_edge(user=user, cache_login=cache_login, short_code="".join(target), media_id=None, output_path=args.output)

            if len(args.target) > 1 and i < len(args.target)-1:
                print(f"Break {args.sleep} secs")
                time.sleep(args.sleep)
    except ValueError as e:
        print(f"Unknow Error: Please change your account whether Instagram soft locked. ({e})")
            
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save the follower of target user data to csv")
    parser.add_argument("--username", type=str, required=True, help="Instagram Username")
    parser.add_argument("--pwd", type=str, required=True, help="Instagram Password")
    parser.add_argument("--target", type=list, nargs="+", required=True, help="Target Instagram post short code")
    parser.add_argument("--output", type=str, help="Output Directory")
    parser.add_argument("--sleep", type=int, default=5, help="Sleep time for each request")
    parser.add_argument("--user_agent", type=str, required=True, help="Please enter your common User Agent")
    parser.add_argument("--cache_login", type=int, default=-1, help="create the .cache folder for reduce the login times")


    args = parser.parse_args()
    
    # print(args.username)
    # print(args.pwd)
    # print(args.target)
    # print(args.output)
    # print(args.user_agent)
    # print(args.sleep)
    main(args)