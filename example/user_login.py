from ig.user import User
from ig.fnc import use_login
import os

def main():
    
    user = User(username="your_username", password="your_pwd", user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")
    # Method 1
    use_login(user)
    print(user.get_target_user(username="photo.khh").__dict__)
    user.logout()    
    
    
    # Method 2 for login
    # two_factor, is_login = user.login()
    
    # if two_factor:
    #     two_factor_code = input("Two factory code: ")
    #     if not user.verify_two_factor(two_factor):
    #         print("Two factory incorrect")
    # elif not is_login:
    #     print("Username or Password incorrect")

if __name__ == "__main__":
    main()