import twint

c = twint.Config()

c.Username = "YahooNewsTopics"
c.Links = "include"
c.Retweets = False

# output
#c.Store_csv = True
c.Store_json = True
c.Output = "YN_tweets.json"

twint.run.Search(c)