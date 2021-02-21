from getpass import getpass, sys
from user import User
from target_user import TargetUser

len_args = len(sys.argv) - 1
if len_args == 0:
    input_user_agent = input("Please enter your User-Agent: ")
    input_username = input("Please enter your username: ")
    input_password = getpass("Please enter your password: ")
    user = User(input_username, input_password, input_user_agent)
    target_username = input("Please enter your target username: ")
else:
    if len_args != 4:
        print("Command Arguments incorrect: python ig_follower2csv.py [username] [password] [Target Username] [User-Agent]")
    else:
        user = User(sys.argv[1], sys.argv[2], sys.argv[4])
        target_username = sys.argv[3]

user.login()
targetUser = TargetUser(target_username, user)
query_hash = input("Please input the query_hash: ")
targetUser.setQueryHash(query_hash)
targetUser.follower2JSON()