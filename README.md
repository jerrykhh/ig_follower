# ig_follower

> Fetching user follower and user following is changed to Instagram Restful API from GraphQL

## Description
It can save the following or follower data based on you is provided Instagram account username (the account must be followed/public account). In addition, the program is able to remove duplicate row or show duplicate only and save to new data file. Moreover, the program can follow the user automatically based on the data file, it will send the follow request to instagram server and for each request can set the customized time interval. User can utilize above method to follow the potential customer for your instagram business promotion/ data analysis.
\* Now Updated version handled is supported the two factor authentication and login challenge (email)

If you interesting this project, you can view my demo video in Youtube(Cantonese) but it is old version:
[Youtube video Click Here](https://youtu.be/7SdcSPcPb8c)

## Features
1. Access the Instagram API via the Code
2. Get User followed/folloer to CSV file
3. Get Instagram Post Liked users to CSV file
4. Combine the CSV file
5. Follow the user automatically based on provided csv file
6. Fetching user details (Testing)


## Installation 
```
pip install -r requirements.txt
```

## Get User followed/follower to CSV file
```
-h, --help            show this help message and exit
--username            Instagram Username
--pwd                 Instagram Password
--target              Target Instagram username
--output              Output Directory (optional)
--sleep               Sleep time for each request (optional, default 5 seconds) (optional)
--user_agent          Please enter your common User Agent
```

## Get user follower to CSV

```
python ig_follower2csv.py --username "your_username" \
    --pwd "your_password" \
    --target "account1" "account2" \
    --output ./output \
    --sleep 5 \
    --user_agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
```

## Get user following to CSV
```
python ig_following2csv.py --username "your_username" \
    --pwd "your_password" \
    --target "account1" "account2" \
    --output ./output \
    --sleep 5 \
    --user_agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
```

## Get Post liked user to CSV file
```
-h, --help            show this help message and exit
--username            Instagram Username
--pwd                 Instagram Password
--target              Target Instagram post short code
--output              Output Directory (optional)
--sleep               Sleep time for each request (optional, default 5 seconds) (optional)
--user_agent          Please enter your common User Agent
```

```
python ig_postliked2csv.py --username "your_username" \
    --pwd "your_password" \
    --target "short_code_1" "short_code_2" \
    --output ./output \
    --sleep 5 \
    --user_agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
```
\* You can find the post short code in the post of user profile page

## Combine the CSV file
```
-h, --help            show this help message and exit
--action              There are merge, drop duplicate, remove followed (merge/drop_dup/rm_fol). Besides, you can use & to finish mulitpe action at same time like 'merge&drop_dup'
--files               Please Enter the file paths (optional)
--output              Saved file path
```

```
python ig_csv.py --action "merge&rm_fol"  \
    --files ./output/file1.csv ./output/file2.csv \
    --output ./output/
```

## Follow the user automatically based on provided csv file
```
-h, --help            show this help message and exit
--username            Instagram Username
--pwd                 Instagram Password
--data                Please enter the path of your datafile
--sleep               Please enter the sleep time for each follow request to avoid the account banned (sec per request), default is 8*60 sec per request (optional)
--log                 Please enter the logging path for insert the logging (optional)
```
```
python ig_follow.py --username "your_username" \
    --pwd "your_password" \
    --user_agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36" \ 
    --data ./output/test-2.csv \
    --log ./output/test-log.txt
```
## Unfollow Users based on provided csv file
```
python ig_unfollow.py --username "your_username" \
    --pwd "your_password" \
    --user_agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36" \ 
    --data ./output/test-2.csv \
    --log ./output/test-log.txt
```
## Fetching User Details (Testing)
```
-h, --help            show this help message and exit
--username            Instagram Username
--pwd PWD             Instagram Password
--user_agent          Please enter your common User Agent
--data DATA           data file (.csv) path [id col is required
--thread THREAD       Number of Threading for fetching (default: 2)
--output OUTPUT       Output Directory
```

```
python ig_biography.py --username "your_username" \
    --pwd "your_password" \
    --user_agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36" \ 
    --data ./output/test-2.csv \
    --thread 3
```
### Limitation
It cannot fetching user information many time when the user is not login, it will redirect to login page. Therefore, the login is required. Also, the ThreadingPool and AsyncIO method is commented due to the too quick to access instagram api. If you want to test just uncomment it. In addition, i tested if set thread 10 the instagram will be temp lock your account.


## Known Limitation
1. if the number of requests >= 200 will print "rate limited" for get the user data to csv file, due to Instagram limited -> Solve: Change the IP address (such as VPN)
2. If your password contain "!" and the Terminal is throw "zsh: parse error near `)'" please use single quota ('') For example: "abcdeGF!" -> 'abcdeGF!'