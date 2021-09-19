import sys
from login import Login
from CSV2Following import CSV2Following

def main():
    len_args = len(sys.argv) - 1
    file_path = None

    if len_args == 0:
        login_panel = Login()
    elif len_args == 3:
        login_panel = Login(sys.argv)
        file_path = sys.argv[3]
    else:
        print("Command Arguments incorrect: python ig_follower2csv.py [username] [password] [CSV filePath]")

    login_panel.login()
    trigger_user = login_panel.getUser()
    CSV2Following(trigger_user).follow()

if __name__ == "__main__":
    main()