import twint

c = twint.Config()

c.Username = "YahooNewsTopics"
c.Links = "include"
c.Retweets = False
c.Since = "2020-06-04 00:00:00"

# output
#c.Store_csv = True
c.Store_json = True
c.Output = "YN_tweets4.json"

twint.run.Search(c)