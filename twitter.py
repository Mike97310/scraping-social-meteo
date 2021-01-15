import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

driver = webdriver.Chrome(executable_path="./chromedriver")
driver.get("https://twitter.com/AustinFC")

# Allow 2 seconds for the web page to open
time.sleep(2)
scroll_pause_time = 2  # time to pause to let information loading
screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
i = 1

# initialisation of html list
html = []

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    for parent in soup.find_all("div", attrs={"data-testid": "tweet"}):
        html.append(parent)
        html = list(dict.fromkeys(html))

    # Break the loop when the height we need to scroll to is larger than the total scroll height
    # or when more 200 tweet have been recorded
    print(len(html))
    if screen_height * i > scroll_height or len(html) > 5000:
        break

tweets = []

for tweet in html:
    #
    try:
        date = tweet.find("time")
        date = date['datetime']
        date = date.replace('T', ' ')
        date = date.replace('Z', "")
        final_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f') - timedelta(hours=6)
        final_date = final_date.strftime("%d/%m/%Y %H:%M:%S")
        array = final_date.split(" ")
        date = array[0]
        time = array[1]

        infos = tweet.find("div", class_="css-1dbjc4n r-18u37iz r-1wtj0ep r-156q2ks r-1mdbhws")
        infos = infos["aria-label"]
        array = infos.split(",")
        comment = array[0]
        comment = comment.split(" ")
        retweet = array[1]
        retweet = retweet.split(" ")
        like = array[2]
        like = like.split(" ")
        tweets.append([comment[0], retweet[1], like[1], date, time])
    except:
        print("tweet couldn't load")


tweets = pd.DataFrame(tweets, columns=['comments', 'retweets', 'likes', 'created date', 'created time'])
tweets = tweets.drop_duplicates()

tweets.to_csv('twitter_AustinFC.csv')

driver.quit()
