import json

def check_if_name_exists(data, nu):
    s = nu.split('\t')
    for x in data['authors']:
        if x['name']==s[0] and x['university']==s[1]:
            return 0
    return 1

def make_edges(id, ids, file):
   for i in ids:
      if(id != i):
         file_edges.write('('+str(id)+','+str(i)+')\n')

# THIRD PART: take the information in the json file and create a file
# containing the "edges" between coauthors

file_json = open('authors.json')
data_json = json.load(file_json)
file_names = open("names.json", "w")
file_universities = open("universities.json", "w")
file_edges = open("edges.txt", "w")

author_names = {}
universities = {}
author_names['authors'] = []
universities['universities'] = []
index = 1;

for idx in range(0,len(data_json['authors'])):
   name = data_json['authors'][idx]['name']
   university = data_json['authors'][idx]['university']
   nu = name+'\t'+university

   if(check_if_name_exists(author_names, nu)):
      author_names['authors'].append({'index': index, 'name': name, 'university': university})
      universities['universities'].append(university)
      author_id = index
      index = index+1
   else:
      for x in author_names['authors']:
          if x['name']==name and x['university']==university:
              author_id = x['index']
   coauthor_indexes = []
   for author in data_json['authors'][idx]['coauthors']:
      nn = author['name']+'\t'+author['university']
      if(check_if_name_exists(author_names, nn)):
         author_names['authors'].append({'index': index, 'name': author['name'], 'university': author['university']})
         universities['universities'].append(author['university'])
         coauthor_indexes.append(index)
         index = index+1
   make_edges(author_id, coauthor_indexes, file_edges)
   ats = list(coauthor_indexes)
   for id in coauthor_indexes:
      ats.remove(id)
      make_edges(id, ats, file_edges)

json.dump(author_names, file_names)
json.dump(universities, file_universities)

file_json.close()
file_names.close()
file_edges.close()
file_universities.close()
