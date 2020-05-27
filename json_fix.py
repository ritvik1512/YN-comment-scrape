import json
import re

with open('YN_tweets.json', 'r') as istr:
    with open('YN_tweets1.json', 'w') as ostr:
        for line in istr:
            line = line.rstrip('\n') + ','
            print(line, file=ostr)