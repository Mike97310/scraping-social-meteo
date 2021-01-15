import twint  # Configure

c = twint.Config()
c.Username = "AustinFC"  # filter by username
c.Limit = 100  # 1 unit = 100 tweets (doesn't seems to load more than 100 anyway)
c.Until = "2019-06-13"  # filter by date
c.Stats = True  # load stats (likes, replies, retweet, ...)
c.Count = True  # show count on terminal
c.Lang = "en"  # language searched
c.Output = "twitter_AustinFC.csv"  # name of the desired output
c.Store_csv = True  # True if you want to save the csv, False otherwise
twint.run.Search(c)  # start the scraping

