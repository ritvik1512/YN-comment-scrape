import json
import re

fcheck = True

with open('YN_tweets4.json', 'r') as istr:
    lines = istr.read().splitlines()
    last = lines[-1]
    with open('YN_tweets_fix.json', 'w') as ostr:
        for line in lines:
            if fcheck:
                line =  "[" + line
                fcheck = False
            line = line.rstrip('\n') + ','
            if line == last:
                line = line.rstrip(",") + ']'
            print(line, file=ostr)