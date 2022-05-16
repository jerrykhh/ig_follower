import json
import requests
from ig.post import Post
from abc import ABC


class Edge(ABC):
    
    def __init__(self, session: requests.Session, page_info_edge_json: json) -> None:
        self.has_next_page: bool = bool(page_info_edge_json["has_next_page"])
        self.end_cursor: str = page_info_edge_json["end_cursor"]
        

class PostEdge(Edge):
    
    def __init__(self, session: requests.Session, post_edge_json: json) -> None:
        super().__init__(session, post_edge_json["page_info"])
        self.post = [Post(session, post["node"]) for post in post_edge_json["edges"]]
            
