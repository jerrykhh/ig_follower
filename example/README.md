# API

You must move the example py file to root of the Project Folder to test it.


## Function
> packages ig.fnc
### use_follow

```
use_follow(user: User, data_file: str, if_err_count_sleep:int=3, sleep:float=8*60, log_path:str = None)

# if_err_count_sleep, if user cannot follow {if_err_count_sleep} times the program will exit

# sleep, Sleep {sleep} seconds for each follow request

# log_path, the path of follow log file

For user follow other users based on provided data file
```

### use_login
```
use_login(user: User)

For user login, it will handled the two factor authentication and the challenge if needed
```

### GraphQL Endpoint

```
conn_graphql_follower_edge(user: User!, username: str!, playload:dict=None, output_path: str="./output")

conn_graphql_following_edge(user: User!, username: str!, playload:dict=None, output_path: str="./output")

conn_graphql_like_edge(user: User!, short_code: str!, playload: dict=None, output_path: str="./output")

# playload, If the playload is None that means Get All the data from First page to Page N
    playload = {
            'shortcode': short_code,
            'include_reel': True,
            'first': 50,
            "after": string # end_cursor, you need to set the this field if you only want start at Page N
        }
# output_path, default is project_folder/output/
```

### Restful API Endpoint
```
conn_restful_follower_api(user: User!, username: str!, playload: dict=None, output_path: str="./output")

conn_restful_following_api(user: User!, username: str!, playload: dict=None, output_path: str="./output")
```

## User

> package: ig.user

### User
```
User:
    --> login(): return need_two_factor: bool, is_login: bool
    --> verify_two_factor( verify_code: str): return code_is_correct: bool
    --> logout(): user_is_logout: bool
    --> clear_session(): void
    --> get_target_user( username: str ): TargetUser
```

### NodeUser
```
NodeUser:
    id: str
    username: str 
    full_name: str 
    profile_pic_url: str 
    followed_by_viewer: bool (None is possible)
    
    --> follow(): return is_followed: bool, response_json: dict
    --> unfollow(): return is_unfollowed: bool, response_json: dict
```

### Preview User
```
PreviewUser extends NodeUser:
    ...
    ALL NodeUser related
    ...
    is_verifiedL bool
```

### General User
```
GeneralUser extends NodeUser:
    ...
    ALL NodeUser related
    ...
    self.is_private: bool
    self.is_verified: bool
    self.requested_by_viewer: bool
    
    --> set_friendship(friendship_json: json): void # if use the restful API repsonsed JSON will not contain the firendship related data so need use this func to update
```


### Target User
```
TargetUser extends GeneralUser:
    
    ...
    All GeneralUser class related
    ...
    
    seo_category_infos: list # 
    biography: str
    blocked_by_viewer: bool
    restricted_by_viewer: bool
        
    follows_viewer: bool
    has_requested_viewer: bool
        
    country_block: bool
    external_url: str
    external_url_linkshimmed :str
    count_followed_by: int
    count_follow: int
    fbid: str (None is possible)
        
    has_ar_effects: bool
    has_clips: bool
    has_guides: bool
    has_channel: bool
    has_blocked_viewer: bool
    highlight_reel_count: int
    hide_like_and_view_counts: bool
        
    is_business_account: bool
    is_professional_account: bool
    is_supervision_enabled: bool
    is_guardian_of_viewer: bool
    is_supervised_by_viewer: bool
    is_embeds_disabled: bool
    is_joined_recently: bool
        
    guardian_id: str
    business_address_json: str
    business_contact_method: str
    business_email: str
    business_phone_number: str
    business_category_name: str
    overall_category_name: str
    category_enum: str
    category_name: str
        
    mutual_followed_by: list
    profile_pic_url_hd: str
    count_highlight: int
        
    count_post: int
    post_edge: PostEdge (not return all post, you need to combine the fnc.conn_graphql_post_edge to get all post)

```

## Edge

> package: ig.edge
```
Edge:
    has_next_page: bool
    end_cursor: str
    
PostEdge extends Edge:
    post: list[Post]
    --> next(): not implement
```

## Post
> package: ig.post
```
Post:
    typeName: str # Post Type
    id: str
    shortcode: str
    display_url: str
    tagged_user = list[PostTaggedUser]
        
    is_video: bool
    comments_disabled: bool
        
    caption: str
    count_comment: int
    posted_timstamp: int
    location: str
        
    count_liked_by: int
    liked_edge: LikeEdge # un implement
    
    --> like(): return isliked: bool
    --> unlike(): return unliked: bool
    --> save(): return isSave: bool
    --> unsave(): return unSave: bool

```

## File
> package: ig.file
```
File
    @static
    -->new(path: str): return pathlib.Path
    
    @static
    -->get_file_dir(): return pathlib.Path(Project Folder)
    
    @static
    -->normailize(row: dict): return Dict # remove the object.__dict__[session] to save the data
    
    @static
    -->append(data: list, output_path: str): void # append the data to output_path
    
```

### CSV Related
```
# For ig_csv.py to execute the action command
CSVProcess:
    actions: list[str]
    file_paths: list[str]
    output_path: str
    
    -->start(): void

CSVProcesser(ABC):
    data: list
    
    @abstractmethod
    -->execute(): void

CSVMerge extends CSVProcesser:
    ...
    ALL CSVProcesser Related    
    ...
    
CSVDropDuplicate extends CSVProcesser:
    ...
    ALL CSVProcesser Related    
    ...

CSVRMFollowed extends CSVProcesser:
    ...
    ALL CSVProcesser Related    
    ...

CSVRead extends CSVProcesser:
    ...
    ALL CSVProcesser Related    
    ...
    
CSVPosting extends CSVProcesser:
    ...
    ALL CSVProcesser Related    
    ...
    
```

## Exception
> package: ig.exception
```
UserLoginFailedException extends Exception
UserLoginChallengeFailed extends UserLoginFailedException
SpamDetectedException extends Exception
```