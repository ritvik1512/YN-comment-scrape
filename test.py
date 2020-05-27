import json
import re

url = []
with open('tweets1.json', 'r') as f:
    res_json = json.load(f)

rlink = re.compile(r'http')
rbracket = re.compile(r'【|】')
kiji = []

for prop in res_json:
    try:
        tweet = prop["tweet"]
        words = tweet.split()

        midashi = tweet[tweet.index("【") + 1:tweet.rindex("】")]
        
        for each in words:
            if rlink.search(each):
                url.append(each)
            elif not rbracket.search(each):
                youyaku = each

        news = midashi, youyaku
        kiji.append(news)

    except:
        pass