import sys
import time
from login import Login
from target_user import TargetUser
from like2csv import Like2CSV

def main():
    len_args = len(sys.argv) - 1

    if len_args == 0:
        login_panel = Login()
    elif len_args == 3:
        login_panel = Login(sys.argv)
    else:
        print("Command Arguments incorrect: python ig_follower2csv.py [username] [password] [Target Username]")

    login_panel.login()
    trigger_user = login_panel.getUser()

    postIds = []

    while True:
        print("If you want to end the input postId, please enter 'start'")
        user_input = input("Please enter post shortcode: ")
        if user_input.lower() == "start":
            break
        else:
            postIds.append(user_input)
    
    if len(postIds) < 1:
        print("Please enter the post shortcode at least 1.")
    else:
        Like2CSV(trigger_user, postIds).save()



if __name__ == "__main__":
    main()