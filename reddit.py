from datetime import datetime, timedelta
import praw
import pandas as pd

# loading of reddit account
reddit = praw.Reddit(client_id='S-Wlacq0w975Lg', client_secret='3z1RIPVHCNRt11_U2c2h6aQ1DCC7qw', user_agent= 'reddit webscriping')

# initialize posts list
posts = []

# get informations from AustinFC subreddit
for post in reddit.subreddit('AustinFC').hot(limit=1000):
    date_to_scrape = post.created
    timestamp = datetime.fromtimestamp(date_to_scrape) - timedelta(hours=7)  # date conversion and jetlag substracted
    final_date = timestamp.strftime('%d/%m/%Y %H:%M:%S')
    array = final_date.split(" ")
    date = array[0]
    time = array[1]
    posts.append([post.title, post.score, post.num_comments, date, time])
# pandas dataframe
posts = pd.DataFrame(posts, columns=['title', 'score', 'num_comments', 'created date', 'created time'])

# add dataframe to csv file named 'movies.csv'
posts.to_csv('reddit_AustinFC.csv')

