import json
import re
import os

regex = re.compile(r'\]\[')

with open("data.json", "r") as f:
    with open("data2.json.tmp", "w") as fw:
        for line in f:
            if regex.match(line):
                line = ','
            fw.write(line)

os.rename('data2.json.tmp', 'data_fix.json')