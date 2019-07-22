import sqlite3
from sqlite3 import Error
import os

def create_table(reddit_post_data):

    try:

        cwd = os.getcwd()
        db = sqlite3.connect(cwd + '\\reddit_data.db')
        cursor = db.cursor()

        print('test')
        cursor.execute('''

            CREATE TABLE IF NOT EXISTS posts (
                num_id integer PRIMARY KEY,
                reddit_data_type text NOT NULL,
                title text NOT NULL,
                reddit_link text NOT NULL,
                subreddit text NOT NULL,
                full_name text NOT NULL,
                post_time integer NOT NULL,
                epoch_time integer NOT NULL
                
            );

            ''')

        db.commit()
        cursor.execute('SELECT MAX(num_id) FROM posts')

        if cursor.fetchone()[0] != None:
            answer = input('Table has data in it. Are you sure you want to overwrite it? (y/n) ')
            if answer == 'y':
                write_new_table(reddit_post_data, db, cursor)

        
        else:
            write_new_table(reddit_post_data, db, cursor)



        

    except Exception as e:
        print(e)

    finally:
        db.close()

def display_table():

    db = sqlite3.connect('reddit_data.db')
    cursor = db.cursor()

    cursor.execute('SELECT * FROM posts')

    print(cursor.fetchall())

def search_table():
    pass

def update_table(reddit_post_data):

    db = sqlite3.connect('reddit_data.db')
    cursor = db.cursor()

    cursor.execute('SELECT full_name FROM posts')
    posts = cursor.fetchall()

    posts_to_add = set()

    for reddit_post in reddit_post_data:
        if reddit_post in posts:
            print('Already in database')
            continue
        posts_to_add.add(reddit_post)
        print('New post added! ' + reddit_post[2])
    
    for new_post in posts_to_add:
        cursor.execute('INSERT INTO posts VALUES (?,?,?,?,?,?,?,?)', new_post)

    db.commit()
    db.close()

def write_new_table(reddit_post_data, db, cursor):

    for single_post_data in reddit_post_data:
        cursor.execute('INSERT INTO posts VALUES (?,?,?,?,?,?,?,?)', reddit_post_data)

    db.commit()
    db.close()


#backup_table

#search_table

#sync_table

#delete_table