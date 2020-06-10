import twint
import sys

c = twint.Config()

# formatting: YY-MM-DD HH:MM:SS
since = sys.argv[1]
until = sys.argv[2]
time = " 00:00:00"

# naming the output json
sinl, unl = since.split("-"), until.split("-")
name = "YN_tweets_" + str(sinl[1])+str(sinl[2]) + "_" + str(unl[1])+str(unl[2]) + ".json"

# input
c.Username = "YahooNewsTopics"
c.Links = "include"
c.Retweets = False
c.Since = str(since) + time
c.Until = str(until) + time

# output
c.Store_csv = True
c.Store_json = True

c.Output = name

# run
twint.run.Search(c)