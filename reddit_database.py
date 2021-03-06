import sqlite3
from sqlite3 import Error
import os

def get_cursor():
    db = sqlite3.connect('reddit_data.db')
    cursor = db.cursor()

    return cursor

def get_db_and_cursor():
    db = sqlite3.connect('reddit_data.db')
    cursor = db.cursor()

    return db, cursor

def get_max_num_id():
    cursor = get_cursor()
    cursor.execute('SELECT MAX(num_id) FROM posts')
    max_num_id = cursor.fetchall()[0][0]

    return max_num_id

def create_table(reddit_post_data):

    try:

        db, cursor = get_db_and_cursor()

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
                write_new_table(reddit_post_data)

        
        else:
            write_new_table(reddit_post_data)

    except Exception as e:
        print(e)

    finally:
        db.close()

def display_table():

    cursor = get_cursor()

    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    print(posts)
    print('Amount of rows: ' + str(len(posts)))

def delete_duplicates():
    db, cursor = get_db_and_cursor()
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()

    cursor.execute('DELETE FROM posts WHERE rowid NOT IN (SELECT MIN(rowid) FROM posts GROUP BY full_name)')
    cursor.execute('SELECT * FROM posts')
    new_posts = cursor.fetchall()

    if len(posts) == len(new_posts):
        print('No duplicates detected. Database unchanged')
    else: 
        print('Success! Duplicates deleted')
    db.commit()

    #Rewrite numbers

   
    for x,y in enumerate(posts):
        values = (x, y[0])
        cursor.execute('''UPDATE posts
                          SET num_id = ? 
                          WHERE num_id = ?''', values)

    db.commit()
    db.close()

def search_table():
    search_fields = ('num_id', 'reddit_data_type', 'title', 'reddit_link', 'subreddit', 'full_name', 'post_time', 'epoch_time')
    search_field_query = ''
    while search_field_query not in search_fields:
        search_field_query = input('What field are you searching for? ')

        if search_field_query == 'exit':
            break

        elif search_field_query not in search_fields:
            print('Data field not in database. Type "exit" to cancel search')

        else:
            search_query = input('What are you searching for? ').strip()
            database_query = '%' + search_query + '%'
            cursor = get_cursor()
            cursor.execute(f'SELECT * FROM posts WHERE {search_field_query}  LIKE ?', (database_query,))

            search_results = cursor.fetchall()
            print(search_results)
            print(f'That returned {len(search_results)} results')

def update_table(reddit_post_data):

    db, cursor = get_db_and_cursor()
    num_id = get_max_num_id() + 1

    cursor.execute('SELECT full_name FROM posts')
    posts = {x[0] for x in cursor.fetchall()}

    posts_to_add = set()

    for reddit_post in reddit_post_data:
        if reddit_post[4] in posts:
            continue
        reddit_post.insert(0, num_id)
        num_id +=1
        reddit_post_tuple = tuple(reddit_post)
        posts_to_add.add(reddit_post_tuple)
        print('New item added! ' + reddit_post_tuple[2])
    
    for new_post in posts_to_add:
        cursor.execute('INSERT INTO posts VALUES (?,?,?,?,?,?,?,?)',  new_post)

    db.commit()
    db.close()

def write_new_table(reddit_post_data):

    db, cursor = get_db_and_cursor()

    for single_post_data in reddit_post_data:
        cursor.execute('INSERT INTO posts VALUES (?,?,?,?,?,?,?,?)', single_post_data)

    db.commit()
    db.close()


#backup_table

#sync_table

#delete_table