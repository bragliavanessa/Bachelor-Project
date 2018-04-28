# coding=utf-8
import json

file = open("university_map_copy.json","r")
data = json.load(file)
print data["TODELETE"]
file.close()
# uni_map = {'USI':['universit','USI','UNIV']}
#
# for i in uni_map:
#     if('universit' in uni_map[i]):
#         print i
