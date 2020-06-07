import sys
import json
import re

# with open(sys.argv[1], encoding='utf-8') as f:
#     data = [line.strip().split('\t') for line in f]
#     with open("input_spe.tsv", "a") as inp:
#         for each in data:
#             inp.write(each[0])
#             inp.write("\n")
#             inp.write(each[1])

inFile = sys.argv[1]
with open(inFile, "r") as op:
    data = json.load(op)
    
# comment = (data[0]["comments"])
# lines = list(comment)
# lines[1] = lines[1]
# print(lines[1])

regex = re.compile(r'agree')

for i in range(len(data)):
    comment = (data[i]["comments"])
    sub = list(comment.values()) # values
    lines = list(comment) # keys

    with open("out1.tsv", "a") as out:
        for j,line in enumerate(lines):

            subc = []

            for elem in sub[j]:
                try:
                    if regex.search(elem):
                        continue
                except TypeError:
                    pass
                #print(elem["reply"])
                subc.append(elem["reply"])

            for sline in subc:
                # main-commentが入力
                line = line.replace('\n', ' ').replace('>', '').replace('＞',  '')
                out.write(line)
                out.write("\t")

                # 返信が出力
                sliner = sline.replace('\n', ' ').replace('>', '').replace('＞',  '')
                out.write(sliner)
                out.write("\n")