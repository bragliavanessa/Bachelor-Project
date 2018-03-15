import os
import json

path = 'catalogs/'

data = {}
data['articles'] = []

for filename in os.listdir(path):
    with open(path+filename) as json_data:
        d = json.load(json_data)
        for x in d['documents']:
            data['articles'].append({
                'id': x['id'],
                'year': x['year'],
                'authors': x['authors'],
                'keywords':x['keywords'],
                'city': x['city'],
                'institution': x['institution']
            })

output_file = open("articles.json", "w")
json.dump(data, output_file)
output_file.close()
