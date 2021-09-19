### Description
It can save the following or follower data based on you is provided Instagram account username (the account must be followed/public account). In addition, the program is able to remove duplicate row or show duplicate only and save to new data file. Moreover, the program can follow the user automatically based on the data file, it will send the follow request to instagram server and for each request can set the customized time interval. User can utilize above method to follow the potential customer for your instagram business promotion/ data analysis.

If you interesting this project, you can view my demo video in Youtube(Cantonese):
[Youtube video Click Here](https://youtu.be/7SdcSPcPb8c)
### Features

- Generate Instagram account follower/following list to CSV
- Compare the CSV File (Different/ identical rows)
- Follow user automatically (follow the CSV file)

### Installation (Follower/ Following to csv)
```
git clone https://github.com/jerrykhh/ig_follower.git
pip install -r requirements.txt
```

### Usage (Follower/ Following to csv)
```
python ig_follower2csv.py
```
Enter following information:
```
Please enter your User-Agent:  Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36
(*Please enter your common Browser)

Please enter your username: this_is_your_username
Password: this_is_your_password
Please enter your target username: target_username
Please input the query_hash: [optional]
```

------

### Usage (Normalize the CSV file)

it will delete your account following or requested user in CSV file
```
python ig_csv2followingfitting.py
```
Enter following information:
```
Please enter your file path: datafile.csv
```
------
### Follow user automatically
```
python ig_csv2following.py
```
Enter following information:
```
Please enter your User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36
(*Please enter your common Browser)
Please enter your username: this_is_your_username
Please enter your password: this_is_your_password
Please enter your file path: this_is_csv_file_path
Please enter the sleeping time (30min = 60sec * 30min = input 1800): [Suggest > 190]
```

### Known Limitation

1. if the number of requests >= 200 will print "rate limited", due to Instagram limited
   Solve: Change the IP address (such as VPN) when the program print following message
   ```
   Follower2CSV: Due to rate limited, program will break 10 sec.
   ```
   