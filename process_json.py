import json
import re
import os
import sys

fcheck = True

open_file =  "YN_tweets_" + sys.argv[1] + ".json"
write_file =  open_file + ".tmp"

with open(open_file, 'r') as istr:
    lines = istr.read().splitlines()
    last = lines[-1]
    
    with open(write_file, 'w') as ostr:
        for line in lines:
            if fcheck:
                line =  "[" + line
                fcheck = False
            line = line.rstrip('\n') + ','
            if line == last:
                line = line.rstrip(",") + ']'
            print(line, file=ostr)

os.rename(write_file, open_file)