### Features

- Generate Instagram account follower/following list to CSV
- Compare the CSV File (Different/ identical rows)
- Follow user automatically (follow the CSV file)

### Installation (Follower/ Following to csv)
```
git clone https://github.com/jerrykhh/ig_follower.git
pip install requests
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