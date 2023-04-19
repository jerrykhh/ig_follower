from ig.user import NodeUser
from ig.file import FetchImageFile, ImageFileSaveQueue
from abc import ABC, abstractmethod


class Feed:
    
    def __init__(self, **entries) -> None:
        
        self.user = NodeUser(None, entries['user'])
        self.items: list[Media] = []
        
        for item in entries['items']:
            try:
                media_type = int(item['media_type'])
                
                if media_type == 8:
                    # Carouse Media
                    self.items.append(CarouselMedia(**item))
                elif media_type == 2:
                    # Video Media
                    self.items.append(VideoMedia(**item))
                elif media_type == 1:
                    # Photo Media
                    self.items.append(PhotoMedia(**item))
                else:
                    print("UnHandle MediaType:", media_type)
            except TypeError as e:
                print("Missing keyword argument", e)

    
    def save_all_media(self, output_path:str):
        
        for item in self.items:
            item.save(output_path)
        
                    

class ImageVersion2Candidate:
        
    def __init__(self, width: int, height: int, url: str, scans_profile=None) -> None:
        self.width = width
        self.height = height
        self.url = url
        self.scans_profile = scans_profile
            
            
class ImageVersion2:

    def __init__(self, image_versions2) -> None:
        self.candidates: list[ImageVersion2Candidate] = [ImageVersion2Candidate(**candidate) for candidate in image_versions2['candidates']]

class VideoVersion:
    
    def __init__(self, height: int, id: str, type: int, url: str, width: int, accessibility_caption:str=None) -> None:
        self.height = height
        self.id = id
        self.type = type
        self.url = url
        self.width = width
    
    def save(self, output_path:str) -> None:
        # type == 101 is mp4
        ImageFileSaveQueue.get_instance().put(FetchImageFile(self.url, output_path, ".mp4", self.id))


class SharingFrictionInfo:
    
    def __init__(self, should_have_sharing_friction: bool, bloks_app_url: str, sharing_friction_payload) -> None:
        self.should_have_sharing_friction = should_have_sharing_friction
        self.bloks_app_url:str = bloks_app_url
        self.sharing_friction_payload = sharing_friction_payload


class CarouselMediaItem:
    
    def __init__(self, id: str, media_type: int, product_type: str, image_versions2: dict, original_width: int, original_height: int, pk: str, carousel_parent_id: str, commerciality_status: str, sharing_friction_info: dict, usertags: dict=None) -> None:
        self.id: str = id
        self.media_type: int = media_type
        self.pk: str = pk
        self.image_versions2: ImageVersion2 = ImageVersion2(image_versions2)
        self.product_type: str = product_type
        self.original_width: int = original_width
        self.original_height: int = original_height
        self.carousel_parent_id: str = carousel_parent_id
        self.commerciality_status: str = commerciality_status
        self.sharing_friction_info: SharingFrictionInfo = SharingFrictionInfo(**sharing_friction_info)
        self.usertags = usertags
        
    @abstractmethod
    def save(self, output_path:str) -> None:
        raise Exception("Not Implement")


class CarouselPhotoMediaItem(CarouselMediaItem):
    
    def __init__(self, id: str, media_type: int, product_type: str, image_versions2: dict, original_width: int, original_height: int, pk: str, carousel_parent_id: str, commerciality_status: str, sharing_friction_info: dict, usertags: dict=None, accessibility_caption: str=None) -> None:        
        super().__init__(id, media_type, product_type, image_versions2, original_width, original_height, pk, carousel_parent_id, commerciality_status, sharing_friction_info, usertags)
        self.accessibility_caption = accessibility_caption

    def save(self, output_path:str):
        id = self.id
        url = self.image_versions2.candidates[0].url
        ImageFileSaveQueue.get_instance().put(FetchImageFile(id=id, url=url, output_path=output_path))

class CarouselVideoMediaItem(CarouselMediaItem):
    
    def __init__(self, id: str, media_type: int, product_type: str, image_versions2: dict, original_width: int, original_height: int, pk: str, carousel_parent_id: str, commerciality_status: str, sharing_friction_info: dict, video_versions, is_dash_eligible:int=None, video_dash_manifest:str=None, video_codec:str=None, video_duration:float=None, number_of_qualities:int=None, has_audio:bool=None, usertags: dict=None, accessibility_caption:str=None) -> None:
        super().__init__(id, media_type, product_type, image_versions2, original_width, original_height, pk, carousel_parent_id, commerciality_status, sharing_friction_info, usertags)
        self.video_versions: list[VideoVersion] = [VideoVersion(**item) for item in video_versions]
        self.video_duration: float = video_duration
        self.is_dash_eligible: int = is_dash_eligible
        self.video_dash_manifest: str = video_dash_manifest
        self.video_codec: str = video_codec
        self.number_of_qualities: int = number_of_qualities
        self.has_audio:bool = has_audio
        
    
    def save(self, output_path:str):
        id = self.id
        url = self.video_versions[0].url
        ImageFileSaveQueue.get_instance().put(FetchImageFile(id=id, url=url, output_path=output_path))
        
        
        


class Media(ABC):
    
    def __init__(self) -> None:
        self.taken_at: int = None
        self.pk: str = None
        self.id: str = None
        self.device_timestamp: int = None
        self.media_type: int = None
        self.code: str = None
        self.client_cache_key: str = None
        self.filter_type: int = None
        self.is_unified_video: bool = None
        self.should_request_ads: bool = None
        self.commerciality_status: str = None
        self.is_paid_partnership: bool = None
        self.is_visual_reply_commenter_notice_enabled: bool = None
        self.clips_tab_pinned_user_ids: list = []
        self.has_delayed_metadata: bool = None
        self.comment_likes_enabled: bool = None
        self.comment_threading_enabled: bool = None
        self.max_num_visible_preview_comments: int = None
        self.has_more_comments: bool = None
        self.preview_comments: list = []
        self.comments: list = None
        self.comment_count: int = None
        self.can_view_more_preview_comments: bool = None
        self.hide_view_all_comment_entrypoint: bool = None
        self.inline_composer_display_condition: str = None
        self.user = None #
        self.can_viewer_reshare: bool = None
        self.can_see_insights_as_brand: bool = None
        self.like_count: int = None
        self.has_liked: bool = None
        self.top_likers: list = []
        self.facepile_top_likers: list = []
        self.is_comments_gif_composer_enabled: bool = None
        # 
        self.original_width: int = None
        self.original_height: int = None
        self.caption = None #
        self.caption_is_edited: bool = None
        self.highlight_post_metadata = None
        self.coauthor_producers = None
        self.coauthor_producer_can_see_organic_insights = None
        self.group = None
        self.is_groups_post_pending_admin_approval = None
        self.invited_coauthor_producers = None
        self.guide_metadata = None
        self.comment_inform_treatment = None #
        self.sharing_friction_info = None # 
        self.original_media_has_visual_reply_media: bool = None
        self.like_and_view_counts_disabled: bool = None
        self.can_viewer_save: bool = None
        self.is_in_profile_grid: bool = None
        self.profile_grid_control_enabled: bool = None
        self.attribution = None
        self.organic_tracking_token: str = None
        self.has_shared_to_fb: int = None
        self.product_type: str = None
        self.show_shop_entrypoint: bool = None
        self.deleted_reason: int = None
        self.integrity_review_decision: str = None
        self.commerce_integrity_review_decision: str = None
        self.music_metadata = None #
        self.is_artist_pick: bool = None
        self.ig_media_sharing_disabled: bool = None
        self.usertags = None #
    
    def setattrs(self, **entries) -> None:
        for k,v in entries.items():
            setattr(self, k, v)
            
    @abstractmethod
    def save(self, output_path:str) -> None:
        raise Exception("Not Implement")

# "media_type": 8
class CarouselMedia(Media):
    
    def __init__(self, **entries) -> None:
        super().__init__()
        self.setattrs(**entries)
        self.carousel_media_count: int = None
        
        
        self.carousel_media = []
        for item in entries['carousel_media']:
            mtype = item['media_type']
            if mtype == 1:
                self.carousel_media.append(CarouselPhotoMediaItem(**item))
            elif mtype == 2:
                self.carousel_media.append(CarouselVideoMediaItem(**item))
            else:
                print("type:", mtype, "not implemented")
        self.carousel_media_ids: list[int] = []
        
    
    def save(self, output_path:str) -> None:
        for item in self.carousel_media:
            item.save(output_path=output_path)
        
    
    
# "media_type": 2

class VideoMedia(Media):
    
    def __init__(self, **entries) -> None:
        super().__init__()
        self.setattrs(**entries)
        self.image_versions2: ImageVersion2 = ImageVersion2(entries['image_versions2']) #
        self.original_width: int = None
        self.original_height : int = None

        self.can_see_insights_as_brand: bool = None
        self.video_subtitles_confidence: float = None
        self.video_subtitles_uri: str = None # url

        self.is_dash_eligible: int = None
        self.video_dash_manifest: str = None # xml
        self.video_codec: str = None
        self.number_of_qualities: int = None
        self.video_versions: list[VideoVersion] = [ VideoVersion(**data) for data in entries['video_versions']]
        self.has_audio: bool = None
        self.video_duration: float = None

        self.clips_metadata = None # 
        self.media_cropping_info = None # 
        

    
    def save(self, output_path:str) -> None:
        self.video_versions[0].save(output_path=output_path)


# "media_type": 1
class PhotoMedia(Media):
    
    def __init__(self, **entries) -> None:
        super().__init__()
        self.setattrs(**entries)
        #
        # self.accessibility_caption = None
        self.photo_of_you: bool = None
        
        #
        self.image_versions2: ImageVersion2 = ImageVersion2(entries['image_versions2']) #
        #
        self.is_organic_product_tagging_eligible: bool = None
        self.can_see_insights_as_brand: bool = None
        #
        
    
    def save(self, output_path:str) -> None:
        id = self.id
        url = self.image_versions2.candidates[0].url
        ImageFileSaveQueue.get_instance().put(FetchImageFile(id=id, url=url, output_path=output_path))
        