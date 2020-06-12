import json
import re
import os
import sys

inFile = sys.argv[1]
regex = re.compile(r'\]\[')

with open(inFile, "r") as f:
    with open("data2.json.tmp", "w") as fw:
        for line in f:
            if regex.match(line):
                line = ','
            fw.write(line)

os.rename('data2.json.tmp', 'data_fix.json')