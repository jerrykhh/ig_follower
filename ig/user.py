import json
import requests
from abc import ABC
from requests import Session
from ig.edge import PostEdge
from ig.exception import UserLoginChallengeFailed, SpamDetectedException
from datetime import datetime
from typing import Tuple


class __USER:
    
    def __init__(self, session: requests.Session) -> None:
        self.session = session
    
    def follow(self, id: str) -> Tuple[bool, dict]:
        res = self.session.post(f"https://www.instagram.com/web/friendships/{id}/follow/", headers={"x-instagram-ajax": "9bcc5b5208c5"})
        json_data = json.loads(res.content)
        if "status" in json_data and json_data["status"] == "ok":
            return True, json_data
        return False, json_data

    def unfollow(self, id: str):
        res = self.session.post(f"https://www.instagram.com/web/friendships/{id}/unfollow/")
        print(res.text)
        json_data = json.loads(res.content)
        if "status" in json_data and json_data["status"] == "ok":
            return True, json_data
        return False , json_data

class NodeUser(__USER):
    
    def __init__(self, session: Session, user_inf: dict):
        super().__init__(session)
        self.id: str = user_inf["id"]
        self.full_name: str = user_inf["full_name"]
        self.username: str = user_inf["username"]
        self.followed_by_viewer: bool = user_inf["followed_by_viewer"] if "followed_by_viewer" in user_inf else None
        self.profile_pic_url: str = user_inf["profile_pic_url"]
      
    
    def follow(self) -> Tuple[bool, dict]:
        if self.followed_by_viewer is not None and not self.followed_by_viewer:
            return super().follow(self.id)
        return False, None
        
    def unfollow(self) -> Tuple[bool, dict]:
        if self.followed_by_viewer is not None and self.followed_by_viewer:
            return super().unfollow(self.id)
        return False, None
        
class PreviewUser(NodeUser):
    
    def __init__(self, session: Session, user_inf: dict):
        super().__init__(session, user_inf)
        self.is_verified: bool =  user_inf["is_verified"]


class GeneralUser(NodeUser):
    
    def __init__(self, session: Session, user_inf: json) -> None:
        super().__init__(session, user_inf)
        self.is_private: bool = user_inf["is_private"]
        self.is_verified: bool = user_inf["is_verified"]
        self.requested_by_viewer: bool = user_inf["requested_by_viewer"] if "requested_by_viewer" in user_inf else None
    
    def follow(self) -> Tuple[bool, dict]:
        if not self.requested_by_viewer:
            return super().follow(self.id)
        return False, None
        
    def unfollow(self) -> Tuple[bool, dict]:
        if self.requested_by_viewer:
            return super().unfollow(self.id)
        return False, None
    
    def set_friendship(self, friendship_json: json):
        self.followed_by_viewer = friendship_json["following"]
        self.requested_by_viewer = friendship_json["outgoing_request"]


class TargetUser(GeneralUser):
    
    def __init__(self, session: requests.Session, inf_json: json) -> None:
        super().__init__(session=session, user_inf=inf_json["graphql"]["user"])
        self.seo_category_infos:list = [ seo[1] for seo in inf_json["seo_category_infos"]]
        inf_json = inf_json["graphql"]["user"]
        self.biography: str = inf_json["biography"]
        self.blocked_by_viewer: bool = inf_json["blocked_by_viewer"]
        self.restricted_by_viewer: bool = inf_json["restricted_by_viewer"]
        
        self.follows_viewer: bool = inf_json["follows_viewer"]
        self.has_requested_viewer: bool = inf_json["has_requested_viewer"]
        
        self.country_block: bool = inf_json["country_block"]
        self.external_url: str = inf_json["external_url"]
        self.external_url_linkshimmed :str = inf_json["external_url_linkshimmed"]
        self.count_followed_by: int = int(inf_json["edge_followed_by"]["count"])
        self.count_follow: int = int(inf_json["edge_follow"]["count"])
        self.fbid: str = inf_json["fbid"]

        
        self.has_ar_effects: bool = inf_json["has_ar_effects"]
        self.has_clips: bool = inf_json["has_clips"]
        self.has_guides: bool = inf_json["has_guides"]
        self.has_channel: bool = inf_json["has_channel"]
        self.has_blocked_viewer: bool = inf_json["has_blocked_viewer"]
        self.highlight_reel_count: int = int(inf_json["highlight_reel_count"])
        self.hide_like_and_view_counts: bool = inf_json["hide_like_and_view_counts"]
        

        self.is_business_account: bool = inf_json["is_business_account"]
        self.is_professional_account: bool = inf_json["is_professional_account"]
        self.is_supervision_enabled: bool  = inf_json["is_supervision_enabled"]
        self.is_guardian_of_viewer: bool = inf_json["is_guardian_of_viewer"]
        self.is_supervised_by_viewer: bool = inf_json["is_supervised_by_viewer"]
        self.is_embeds_disabled: bool = inf_json["is_embeds_disabled"]
        self.is_joined_recently: bool = inf_json["is_joined_recently"]
        
        self.guardian_id: str = inf_json["guardian_id"]
        self.business_address_json: str = inf_json["business_address_json"]
        self.business_contact_method: str = inf_json["business_contact_method"]
        self.business_email: str = inf_json["business_email"]
        self.business_phone_number: str = inf_json["business_phone_number"]
        self.business_category_name: str = inf_json["business_category_name"]
        self.overall_category_name: str = inf_json["overall_category_name"]
        self.category_enum: str = inf_json["category_enum"]
        self.category_name: str = inf_json["category_name"]
        
        self.mutual_followed_by: list = [user["node"]["username"] for user in inf_json["edge_mutual_followed_by"]["edges"]]
       
        self.profile_pic_url_hd: str = inf_json["profile_pic_url_hd"]
        
        self.count_highlight: int = inf_json["edge_felix_video_timeline"]["count"]
        # url not implement
        
        self.count_post: int = inf_json["edge_owner_to_timeline_media"]["count"]
        self.post_edge: PostEdge = PostEdge(session, inf_json["edge_owner_to_timeline_media"])
        

class User(__USER):
    
    def __init__(self, username: str, password: str, user_agent: str) -> None:
        super().__init__(requests.Session())
        self.username = username
        self.password = password
        
        self.two_factore_info = None
        self.session.get('https://www.instagram.com/accounts/login/')
        self.session.headers.update({
            'User-agent': user_agent,
            'x-csrftoken': self.session.cookies['csrftoken']
        })
        print(f"csrftoken: {self.session.cookies['csrftoken']}")
        self.is_login = False
        self.is_logout = False
    
        
    def login(self):
        time = int(datetime.now().timestamp())
        res = self.session.post('https://www.instagram.com/accounts/login/ajax/', 
                          data={
                                'username': self.username,
                                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{self.password}',
                                'queryParams': {},
                                'optIntoOneTap': 'false'
                            }, headers={
                            "X-Requested-With": "XMLHttpRequest",
                            "Referer": "https://www.instagram.com/accounts/login/"
                        }, timeout=5)

        two_factor = False
        
        try:
            res_data = json.loads(res.text)
            # {'user': True, 'userId': '6008916655', 'authenticated': True, 'oneTapPrompt': True, 'status': 'ok'}
            print(res_data)
            if str(res_data['status']).lower() == 'ok':
                if res_data["authenticated"]:
                    self.session.headers.update({
                        'x-csrftoken': self.session.cookies['csrftoken']
                    })
                    self.is_login = True
            else:
                # print(res_data)
                # {'message': '', 'two_factor_required': True, 'two_factor_info': {'pk': 4261114159, 'username': 'photo.khh', 'sms_two_factor_on': False, 'whatsapp_two_factor_on': False, 'totp_two_factor_on': True, 'eligible_for_multiple_totp': True, 'obfuscated_phone_number': '2428', 'two_factor_identifier': 'KJnUvq45y8MFr7OWt7GYBduM8SGAJocmoDtlHOgLrLmjg3hbjinMMBHeC5Z42EDw', 'show_messenger_code_option': False, 'show_new_login_screen': True, 'show_trusted_device_option': False, 'should_opt_in_trusted_device_option': True, 'pending_trusted_notification': False, 'sms_not_allowed_reason': None, 'trusted_notification_polling_nonce': None, 'is_trusted_device': False, 'phone_verification_settings': {'max_sms_count': 2, 'resend_sms_delay_sec': 60, 'robocall_count_down_time_sec': 30, 'robocall_after_max_sms': True}}, 'phone_verification_settings': {'max_sms_count': 2, 'resend_sms_delay_sec': 60, 'robocall_count_down_time_sec': 30, 'robocall_after_max_sms': True}, 'status': 'fail', 'error_type': 'two_factor_required'}
                
                if "checkpoint_url" in res_data:
                    # raise UserLoginDiffDeciveException()
                    self.is_login = self.__handle_challenge(res_data["checkpoint_url"])
                
                if "spam" in res_data and res_data["spam"]:
                    raise SpamDetectedException()
                
                if "two_factor_required" in res_data and res_data['two_factor_required']:
                    self.two_factore_info = res_data['two_factor_info']
                    two_factor = True
                
                
        except ValueError as e:
            raise e
        
        return two_factor, self.is_login
    
    def __handle_challenge(self, checkpoint_url: str):
        # choice 1 will be sent the email
        print(f"https://www.instagram.com{checkpoint_url}")
        res_data = self.session.post(f"https://www.instagram.com{checkpoint_url}", data={"choice": "1"}, headers={"x-instagram-ajax": "9bcc5b5208c5"})
        print(res_data)
        print(res_data.content)
        res_data = json.loads(res_data.content)
        print(f"The verify code is sent to {res_data['fields']['contact_point']} ({res_data['fields']['form_type']})")
        verify_code = input("Please enter received veify code: ")
        res = self.session.post(f"https://www.instagram.com{res_data['navigation']['forward']}", data={"security_code": verify_code})
        
        if res.status_code == 200:
            return True
        
        raise UserLoginChallengeFailed()
        # raise UserLoginChallengeFailed()
        # send the verify code to server
        
    # def check_session_isLogin(self):
    #     res_data = self.session.get("https://i.instagram.com/api/v1/direct_v2/get_badge_count/?no_raven=1")
    #     print("check_session_isLogin:",res_data)
    #     if res_data.status_code == 200:
    #         try:
    #             json_data = json.loads(res_data.text)
    #             if "user_id" in json_data:
    #                 return True
    #         except:
    #             pass
    #     return False

        
    
    def verify_two_factor(self, verify_code: str) -> bool:
        if self.two_factore_info is not None:
            res = self.session.post('https://www.instagram.com/accounts/login/ajax/two_factor/',
                                    data={
                                        'identifier': self.two_factore_info['two_factor_identifier'],
                                        'trust_signal': True,
                                        'username': self.username,
                                        'verificationCode': verify_code
                                    }, timeout=5)
            # {'authenticated': True, 'userId': '4261114159', 'oneTapPrompt': True, 'status': 'ok'}
            res_data = json.loads(res.text)
            if str(res_data['status']).lower() != 'ok':
                return False
            self.session.headers.update({
                        'x-csrftoken': self.session.cookies['csrftoken']
                    })
            self.is_login = True
        return True
    
    # def __del__(self):
    #     try:
    #         if not self.is_logout:
            
    #             if not self.logout():
    #                 print("Logout failed")
    #             else:
    #                 print("Logout successful")
    #     except:
    #         pass
        
            
    def logout(self) -> bool:
        res = self.session.post('https://www.instagram.com/accounts/logout/ajax/',
                                data={
                                    'one_tap_app_login': 0,
                                    'user_id': self.session.cookies['ds_user_id']
                                },
                                headers={
                                    'x-csrftoken': self.session.cookies['csrftoken'],
                                    'content-type': 'application/x-www-form-urlencoded',
                                    'referer': 'https://www.instagram.com/accounts/onetap/?next=%2F'
                                }, timeout=5)

        if json.loads(res.content)['status'] == 'ok':
            self.is_logout = True
            self.is_login = False
            return True
        return False
    
    def __chk_login(self):
        if not self.login:
            raise Exception("Please login")
    
    
    def get_target_user(self, username: str) -> TargetUser:

        self.__chk_login()
         
        # QUERY_HASH = "69cba40317214236af40e7efa697781d"
        # variables = {
        #     "id": "339326942",
        #     "first": 50
        # }
        res_data = self.session.get(f"https://www.instagram.com/{username}/?__a=1&__d=dis", timeout=10)
        res_data = json.loads(res_data.content)
        if not bool(res_data):
            return None
        
        return TargetUser(self.session, res_data)
    
    def clear_session(self):
        self.session.cookies.clear()
        self.is_login = False
        self.is_logout = False
 


    
# class TargetPost:
    
#     def __init__(self, post_id: str) -> None:
#         self.post_id = post_id
    
#     def save_like_to_csv(self, output_path:str) -> None:
        