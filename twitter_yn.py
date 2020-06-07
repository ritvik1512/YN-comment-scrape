import twint

c = twint.Config()

c.Username = "YahooNewsTopics"
c.Links = "include"
c.Retweets = False
c.Since = "2020-06-07 15:41:17"

# output
#c.Store_csv = True
c.Store_json = True
c.Output = "YN_tweets_0607_1.json"

twint.run.Search(c)