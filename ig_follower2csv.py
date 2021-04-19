import sys
from login import Login
from target_user import TargetUser
from follower2csv import Follower2CSV

len_args = len(sys.argv) - 1

if len_args == 0:
    login_panel = Login()
elif len_args == 3:
    login_panel = Login(sys.argv)
else:
    print("Command Arguments incorrect: python ig_follower2csv.py [username] [password] [Target Username]")

login_panel.login()
trigger_user = login_panel.getUser()
while(True):
    Follower2CSV(TargetUser(trigger_user), trigger_user).save()