import sys
import time
from login import Login
from target_user import TargetUser
from following2csv import Following2CSV

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
    target_user = TargetUser(trigger_user)
    Following2CSV(target_user, trigger_user).save()
    print("break 5 sec, due to avoid to ban account")
    del target_user
    time.sleep(5)