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
    num_id = 0
    posts = list()

    response = requests.get(f'https://oauth.reddit.com/user/{cred.username}/saved.json?limit={num_posts}', headers=headers)

    posts, num_id, after = parse_json(response.json(), posts, num_id)
    

    while after != None:
        response = requests.get(f'https://oauth.reddit.com/user/{cred.username}/saved.json?limit={num_posts}&after={after}', headers=headers)

        posts, num_id, after = parse_json(response.json(), posts, num_id)
        print(num_id,after)

    return posts

def parse_json(json_data, data_listings, num_id):
    
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
        #dont forget to havebody = item['data']['body']
        

        post_listing = (num_id, saved_type, title, link, subreddit, full_name, post_time, epoch_time)
        data_listings.append(post_listing)
        num_id += 1

    after = json_data['data']['after']


    return data_listings, num_id, after


def main():


    command_list = {

        'create' : lambda: reddit_database.create_table(get_saved_posts()),
        'print' : lambda: reddit_database.display_table(),
        'update' : lambda: reddit_database.update_table(get_saved_posts())
    }

    command = sys.argv[1]
    command_list[command]()




if __name__ == '__main__':
    main()
