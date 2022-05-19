from ig.file import File, CSVRead
from ig.user import User, GeneralUser
from pathlib import Path
from datetime import datetime
from ig.exception import UserLoginFailedException, RequestRateLimitedException, RequestOverException
import pandas as pd
import requests
import json
import time
import sys

GRAPHQL_QUERY_ENDPOINT = "https://www.instagram.com/graphql/query/"
RESFUL_API_ENPOINT = "https://i.instagram.com/api/v1/"

def use_login(user: User):
    if not user.is_login:
        two_factor, logined = user.login()
        
        if two_factor:
            __login_two_factor(user)
        elif not logined:
            raise UserLoginFailedException()
        
def __login_two_factor(user: User):
    print("Two factor authentication is required")
    count: int = 0
    while(not user.verify_two_factor(input("Please Enter Two Factor Code: "))):
        count+=1
        if count >= 3:
            sys.exit(1)  

def __conn_grahql(session: requests.Session, url: str ) -> json or None:
    
    over_count = 0
    while True:
        try:
            res = session.get(url, timeout=5)
            json_data = json.loads(res.content)
            if bool(json_data) and json_data["status"] == "ok" :
                return json_data["data"]
            elif not bool(json_data):
                print(f"Response Empty, {json_data}")
            elif json_data["status"] != "ok":
                if json_data['message'] == 'rate limited':
                    raise RequestRateLimitedException()
                if json_data['message'] == 'Please wait a few minutes before you try again.':
                    raise RequestRateLimitedException()
                print(f"Unknow Error, res={json_data}")
            
            return None
        except json.decoder.JSONDecodeError or ValueError:
            print("Instagram is limited ~200 request, please change your IP address (VPN/ Proxy/ ...) if you want to contiune")
            time.sleep(10)
        except RequestOverException:
            print(f"Your request > 200, need to wait a few minutes before you try again. Sleep {60*3*over_count} seconds")
            over_count+=1
            time.sleep(60*3*over_count)
            
        except RequestRateLimitedException:
            print("Instagram is limited ~200 request, please change your IP address (VPN/ Proxy/ ...) if you want to contiune")
            time.sleep(10)
        except requests.exceptions.RequestException:
            print(f"Waiting Connection (Sleep 10 secs), please check you network ({datetime.now().strftime('%d %m %Y %H:%M:%S')})")
            time.sleep(10)

def conn_graphql_like_edge(user:User, short_code:str, playload:dict=None, output_path: str=f"{File.get_file_dir()}/output", query_hash:str="d5d763b1e2acf209d62d22d184488e57"):

    path = Path(output_path)

    use_login(user)
    
    if not path.exists() or path.is_dir():
        output_path = f"{output_path}/likedpost-{short_code}-{datetime.now().strftime('%d%m%YT%H%M%S')}.csv"
    
    
    if playload is None:
        playload = {
            'shortcode': short_code,
            'include_reel': True,
            'first': 50
        }
    
    res = __conn_grahql(user.session, url=f"{GRAPHQL_QUERY_ENDPOINT}?query_hash={query_hash}&variables={json.dumps(playload)}")
    if res is not None: 
        
        shortcode_media = res["shortcode_media"] 
        if shortcode_media is not None:
            edge = shortcode_media["edge_liked_by"]
            liked_users = [GeneralUser(user.session, liked_user["node"]) for liked_user in edge["edges"]]
            File.append(data=liked_users, output_path=f"{output_path}")
            
            page_info = edge["page_info"]
            if bool(page_info["has_next_page"]):
                    playload["after"] = page_info["end_cursor"]
                    print(f"{len(liked_users)} found, has next: False")
                    conn_graphql_like_edge(user, short_code, playload, output_path)
            else:
                print(f"{len(liked_users)} found, has next: False")
        else:
            print(f"{short_code}: null found.")

def conn_graphql_follower_edge(user: User, username: str, user_id:str=None, playload:dict=None, output_path: str=f"{File.get_file_dir()}/output", query_hash:str="5aefa9893005572d237da5068082d8d5"):
    
    path = Path(output_path)

    use_login(user)
    
    if user_id is None:
        target_user = user.get_target_user(username)
        user_id = target_user.id

    if not path.exists() or path.is_dir():
        output_path = f"{output_path}/{username}-follower-{datetime.now().strftime('%d%m%YT%H%M%S')}.csv"
        
    if playload is None:
        playload = {
            'id': user_id,
            'include_reel': False,
            'fetch_mutual': False,
            'first': 50
        }
            
    res = __conn_grahql(user.session, url=f"{GRAPHQL_QUERY_ENDPOINT}?query_hash={query_hash}&variables={json.dumps(playload)}")
    if res is not None:
        res_user = res["user"] 
        if res_user is not None:
            edge = res_user["edge_followed_by"]
            followered_users = [GeneralUser(user.session, followered_user["node"]) for followered_user in edge["edges"]]
            File.append(data=followered_users, output_path=f"{output_path}")
            
            page_info = edge["page_info"]
            if bool(page_info["has_next_page"]):
                print(f"{len(followered_users)} found, has next: True")
                playload["after"] = page_info["end_cursor"]
                conn_graphql_follower_edge(user, username, user_id, playload, output_path)
            else:
                print(f"{len(followered_users)} found, has next: False")
        else:
            print(f"{username}: null found.")
    
def conn_graphql_following_edge(user: User, username: str, user_id:str=None, playload:dict=None, output_path: str=f"{File.get_file_dir()}/output", query_hash:str="3dec7e2c57367ef3da3d987d89f9dbc8"):
    
    path = Path(output_path)

    use_login(user)
    
    if user_id is None:
        target_user = user.get_target_user(username)
        user_id = target_user.id

    if not path.exists() or path.is_dir():
        output_path = f"{output_path}/{username}-following-{datetime.now().strftime('%d%m%YT%H%M%S')}.csv"
        
    if playload is None:
        playload = {
            'id': user_id,
            'include_reel': False,
            'fetch_mutual': False,
            'first': 50
        }
            
    res = __conn_grahql(user.session, url=f"{GRAPHQL_QUERY_ENDPOINT}?query_hash={query_hash}&variables={json.dumps(playload)}")
    if res is not None:
        res_user = res["user"] 
        if res_user is not None:
            edge = res_user["edge_follow"]
            following_users = [GeneralUser(user.session, following_user["node"]) for following_user in edge["edges"]]
            File.append(data=following_users, output_path=f"{output_path}")
            
            page_info = edge["page_info"]
            if bool(page_info["has_next_page"]):
                    print(f"{len(following_users)} found, has next: True")
                    playload["after"] = page_info["end_cursor"]
                    conn_graphql_follower_edge(user, username, user_id, playload, output_path)
            else:
                print(f"{len(following_users)} found, has next: False")
        else:
            print(f"{username}: null found.")

def __conn_resful(session: requests.Session, url: str, app_id:str="936619743392459") -> json or None:
    while True:
        try:
            res = session.get(url, timeout=5, headers={"x-ig-app-id": app_id})
            json_data = json.loads(res.content)
            if bool(json_data) and json_data["status"] == "ok" :
                return json_data
            elif not bool(json_data):
                print(f"Response Empty, {json_data}")
            elif json_data["status"] != "ok":
                print(f"Unknow Error, res={json_data}")
            
            return None
        except requests.exceptions.RequestException as e:
            print(e)
            print(f"Waiting Connection (Sleep 10 secs), please check your network ({datetime.now().strftime('%d %m %Y %H:%M:%S')})")
            time.sleep(10)

def __conn_resful_showmany(session: requests.Session, url: str, data: dict, app_id:str="936619743392459"):
    print(data)
    
    while True:
        try:
            res = session.post(url, timeout=5, data=data, headers={
                "content-type": "application/x-www-form-urlencoded",
                "x-ig-app-id": app_id})
            print(res)
            json_data = json.loads(res.content)
            if bool(json_data) and json_data["status"] == "ok" :
                return json_data
            elif not bool(json_data):
                print(f"Response Empty, {json_data}")
            elif json_data["status"] != "ok":
                print(f"Unknow Error, res={json_data}")
            
            return None
        except requests.exceptions.RequestException as e:
            print(e)
            print(f"Waiting Connection (Sleep 10 secs), please check your network ({datetime.now().strftime('%d %m %Y %H:%M:%S')})")
            time.sleep(10)

def __resful_api_normailize(session: requests.Session, users_data: json) -> list:
    
    users = {}
    for followed_user in users_data:
        node = GeneralUser(session, followed_user)
        users[str(node.id)] = node

    showmany_res = __conn_resful_showmany(session, f"{RESFUL_API_ENPOINT}friendships/show_many/", data={"user_ids":  ",".join(users)})
    if showmany_res is not None:
        friendship = showmany_res["friendship_statuses"]
        for key in friendship.keys():
            users[str(key)].set_friendship(friendship[key])
    
        return [users[str(key)] for key in users.keys()]
    return []

def __payload_to_query(playload: dict) -> str:
    q: str = ""
    for key in playload.keys():
        q += f"{key}={playload[key]}&"
    return q[0: len(q)-1]
    
def conn_restful_follower_api(user: User, username: str, user_id:str=None, playload: dict=None, output_path: str=f"{File.get_file_dir()}/output"):
    
    path = Path(output_path)
    
    use_login(user)
    
    if user_id is None:
        target_user = user.get_target_user(username)
        user_id = target_user.id
    
    if not path.exists() or path.is_dir():
        output_path = f"{output_path}/{username}-follower-{datetime.now().strftime('%d%m%YT%H%M%S')}.csv"
        
    
    if playload is None:
        
        playload = {
            "count": 42,
            "search_surface": "follow_list_page"
        }
    
    q: str = __payload_to_query(playload)
    res = __conn_resful(user.session, url=f"{RESFUL_API_ENPOINT}friendships/{user_id}/followers/?{q}")
    # print(res)
    if res is not None:
        
        next_max_id = res["next_max_id"] if "next_max_id" in res else None
        data = __resful_api_normailize(user.session, res["users"])
        File.append(data, output_path=f"{output_path}")
        if next_max_id is not None:
            playload["max_id"] = next_max_id
            print(f"{len(data)} found, has next: True")
            conn_restful_follower_api(user, username, user_id, playload, output_path)
        else:
            print(f"{len(data)} found, has next: False")
            
def conn_restful_following_api(user: User, username: str, user_id:str=None, playload: dict=None, output_path: str=f"{File.get_file_dir()}/output"):
    
    path = Path(output_path)
    
    use_login(user)
    
    if user_id is None:
        target_user = user.get_target_user(username)
        user_id = target_user.id
    
    if not path.exists() or path.is_dir():
        output_path = f"{output_path}/{username}-following-{datetime.now().strftime('%d%m%YT%H%M%S')}.csv"
        
    
    if playload is None:
        
        playload = {
            "count": 42
        }
    
    q: str = __payload_to_query(playload)
    res = __conn_resful(user.session, url=f"{RESFUL_API_ENPOINT}friendships/{user_id}/following/?{q}")
    # print(res)
    if res is not None:
        # print(res["users"])
        next_max_id = res["next_max_id"] if "next_max_id" in res else None
        data = __resful_api_normailize(user.session, res["users"])
        # print(data)
        File.append(data, output_path=output_path)
        
        if next_max_id is not None:
            print(f"{len(data)} found, has next: True")
            playload["max_id"] = next_max_id
            conn_restful_following_api(user, username, user_id, playload, output_path)
        else:
            print(f"{len(data)} found, has next: False")

def __logging(data: str, logging_path:str):
    if logging_path is not None:
        fp = open(logging_path, mode="a+")
        fp.write(f"{datetime.now().strftime('%d%m%YT%H%M%S')}: {data}\n")
        fp.close()
        
def use_follow(user: User, data_file: str, if_err_count_sleep:int=3, sleep:float=8*60, log_path:str = None):
    use_login(user)
    df: pd.DataFrame = CSVRead([data_file]).execute().pop()
    error_count = 0
    
    i = 0
    while i < len(df):
        
        result, res = user.follow(df['id'][i])
        if not result:
            
            if "spam" in res and res["spam"]:
                print("Program END: Instagram may blocked your account follow function.")
                __logging(f"Program END: Spam detected, instagram may blocked your account follow function. ({res})", log_path)
            else:
                
                sleep_sec = 60*10 # 10min
                
                if error_count == if_err_count_sleep:
                    print(f"Failed {error_count} times, it will sleep 3 hours")
                    __logging(f"Failed {error_count} times, it will sleep 3 hours. ({res})", log_path)
                    sleep_sec = 60*60*3
                    i+=1
                elif error_count == if_err_count_sleep+1:
                    print(f"Program END: try {if_err_count_sleep}+1 times it still error")
                    __logging(f"Program END: try {if_err_count_sleep}+1 times it still error. ({res})", log_path)
                    exit(1)
                else:
                    
                    print("Request Error: Due to the server request blocked, it will sleep 10min")
                    __logging(f"Request Error: Due to the server request blocked, it will sleep 10min and login again. ({res})", logging_path=log_path)
                    print("Login again.")
                    try:
                        user.logout()
                    except:
                        pass
                    
                    try:
                        user.clear_session()
                        user.login()
                    except:
                        print("Program END: Session restart failed")
                        __logging("Program END: Session restart failed. ({res})", log_path)
                        exit(1)
                time.sleep(sleep_sec)
                error_count+=1
        else:
            
            print(f"{res['result']} {df['username'][i]} ({df['id'][i]}) at {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
            __logging(f"{res['result']} {df['username'][i]} ({df['id'][i]}). ({res})", log_path)
            i+=1
            
            if i < len(df):
                time.sleep(sleep)
    
    
    print(f"Task Finish, total: {len(df)} rows")
    __logging(f"Task Finish, total: {len(df)} rows", log_path)
                