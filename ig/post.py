import json
import requests
import ig.user as user


class Post:
    
    def __init__(self, session: requests.Session, post_json: json) -> None:
        self.session = session
        
        self.typeName: str = post_json["__typename"]
        self.id: str = post_json["id"]
        self.shortcode: str = post_json["shortcode"]
        self.display_url: str = post_json["display_url"]
        self.tagged_user = [user.PreviewUser(session, user["node"]["user"]) for user in post_json["edge_media_to_tagged_user"]["edges"]]
        
        self.is_video: bool = post_json["is_video"]
        self.comments_disabled: bool = bool(post_json["comments_disabled"])
        
        self.caption: str = ' '.join([caption["node"]["text"] for caption in post_json["edge_media_to_caption"]["edges"]])
        self.count_comment: int = int(post_json["edge_media_to_comment"]["count"])
        self.posted_timstamp = int(post_json["taken_at_timestamp"])
        self.location: str = post_json["location"]
        
        self.count_liked_by: int = int(post_json["edge_liked_by"]["count"])
        # self.liked_edge: LikeEdge = None
    
    def like(self) -> bool:
        res_data = json.loads(self.session.post(f"https://www.instagram.com/web/likes/{self.id}/like/").content)
        if "status" in res_data and res_data["status"] == "ok":
            return True
        return False
    
    def unlike(self) -> bool:
        res_data = json.loads(self.session.post(f"https://www.instagram.com/web/likes/{self.id}/unlike/").content)
        if "status" in res_data and res_data["status"] == "ok":
            return True
        return False
    
    def save(self) -> bool:
        res_data = json.loads(self.session.post(f"https://www.instagram.com/web/save/{self.id}/save/").content)
        if "status" in res_data and res_data["status"] == "ok":
            return True
        return False
    
    def unsave(self) -> bool:
        res_data = json.loads(self.session.post(f"https://www.instagram.com/web/save/{self.id}/unsave/").content)
        if "status" in res_data and res_data["status"] == "ok":
            return True
        return False