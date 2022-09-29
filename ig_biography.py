import argparse
import asyncio
from ig.fnc import use_get_user_biography
from ig.user import User

def main(args):
    user = User(username=args.username, password=args.pwd, user_agent=args.user_agent)
    
    
    if args.output is None:
        use_get_user_biography(user=user, data_file=args.data, max_thread=args.thread)
    else:
        use_get_user_biography(user=user, data_file=args.data, max_thread=args.thread, output_path=args.output)
    
    # loop = asyncio.get_event_loop()
    # future = asyncio.ensure_future(use_get_user_biography(
    #     data_file=args.data,
    #     max_thread=args.thread,
    #     output_path=args.output
    # ))
    # loop.run_until_complete(future)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ig_follower: Fetch User Details")
    parser.add_argument("--username", type=str, required=True, help="Instagram Username")
    parser.add_argument("--pwd", type=str, required=True, help="Instagram Password")
    parser.add_argument("--user_agent", type=str, required=True, help="Please enter your common User Agent")
    parser.add_argument("--data", type=str, required=True, help="data file (.csv) path [id col is required")
    parser.add_argument("--thread", type=int, default=2, help="Number of Threading for fetching (default: 4)")
    parser.add_argument("--output", type=str, default=None,help="Output Directory")
    args = parser.parse_args()
    main(args)