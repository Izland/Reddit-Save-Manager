import credentials as cred
import reddit_database
import requests
import requests.auth
import sys
import time

def get_token(client_id, client_secret, username, password):
    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    post_data = {'grant_type' : 'password', 'username' : username, 'password' : password}
    headers = {'User-Agent' : 'RedditSavedPostViewer/0.2 by u/blu_shrike'}
    response = requests.post('https://www.reddit.com/api/v1/access_token', auth=client_auth, data=post_data, headers=headers)
    
    return response.json()['access_token']

def get_saved_posts():
    token = get_token(cred.client_id, cred.client_secret, cred.username, cred.password)
    headers = {'Authorization' : 'bearer ' + token, 'User-Agent': 'RedditSavedPostViewer/0.2 by u/blu_shrike'}
    num_posts = 100
    posts = list()

    response = requests.get(f'https://oauth.reddit.com/user/{cred.username}/saved.json?limit={num_posts}', headers=headers)

    posts, after = parse_json(response.json(), posts)
    

    while after != None:
        response = requests.get(f'https://oauth.reddit.com/user/{cred.username}/saved.json?limit={num_posts}&after={after}', headers=headers)

        posts, after = parse_json(response.json(), posts,)
        print(after)

    return posts

def parse_json(json_data, data_listings):
    
    reddit_url = 'https://www.reddit.com'


    for item in json_data['data']['children']:

        if item['kind'] == 't1':
            saved_type = 'Comment'
            full_name = "t1_" + item["data"]["id"]
            title = item['data']['link_title']

        elif item['kind'] == 't3':
            saved_type = 'Post'
            full_name = "t3_" + item["data"]["id"]
            title = item['data']['title']

        else: 
            saved_type = 'Unknown'

        link = reddit_url + item['data']['permalink']
        subreddit = item['data']['subreddit_name_prefixed'].lower()
        post_time = time.ctime(item['data']['created_utc'])
        epoch_time = item['data']['created_utc']
        

        post_listing = [saved_type, title, link, subreddit, full_name, post_time, epoch_time]
        data_listings.append(post_listing)

    after = json_data['data']['after']


    return data_listings, after


def main():


    command_list = {

        'create' : lambda: reddit_database.create_table(get_saved_posts()),
        'print' : lambda: reddit_database.display_table(),
        'search' : lambda: reddit_database.search_table(),
        'update' : lambda: reddit_database.update_table(get_saved_posts()),
        'test' : lambda: reddit_database.delete_duplicates()
    }

    try:
        assert len(sys.argv) == 2
        command = sys.argv[1]
        command_list[command]()

    except AssertionError:
        print('Type only ONE command after ./main.py')
        




if __name__ == '__main__':
    main()
