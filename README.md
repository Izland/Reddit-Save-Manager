# Reddit-Save-Manager

Reddit has a lot of useful information on it, and if you're like me, you save A LOT of posts and comments. Unfortunately, most people don't know that Reddit only keeps track of the last ~1000 or so saved items, so when you go over that limit, any saved content outside of those last entries get much harder to find. This application is a personal project designed to permanently save your Reddit saved content by storing it in a local database on your computer.

Requires a Reddit account, a client id and a client secret. You must also create a .ini file called credentials.ini to be placed in the main folder with the following format:

[credentials]
client_id=XXXXXX
client_secret=XXXXXX
username=XXXXXX
password=XXXXXX

Program usage is as follows:

python .\main.py [command]

Commands for users are:

"create" - Use if you are creating your database for the first time. Note that it will ask you if you want to overwrite data if the table has already been filled.
"print" - Shows data for all saved items in database.
"search" - Queries database based on the field you are searching for and the actual search term. Search fields include 'num_id', 'reddit_data_type', 'title',                             reddit_link', 'subreddit', 'full_name', 'post_time', and 'epoch_time'.
"update" - If you have saved posts/comments on reddit since you have last updated the database, then this command will add those entries to the database.
