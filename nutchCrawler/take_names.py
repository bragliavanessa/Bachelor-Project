# Lets use a regular expression to extract members' names
# from the crawled html pages
import re
import os
import json

# Remove unnecessary content and excess spaces
def to_plane_text(fileLine):
   fileLine = (re.sub(' +',' ', fileLine.replace('\n', ' ').replace('\t',' ').replace("<em>", ' ').replace('</EM>', ' ').replace('</S>', ' ').replace('<img src="../updated.gif" alt="updated">', ' ')))
   return fileLine


# Take only the Switzerland researchers and same them tomporarily in a file
def split_lines(fileLine):
   components = fileLine.split(';')
   res = ""
   for x in components:
	   if 'Switzerland' in x:
		   res = res + x + ';';
   if res != "":
      file_result.write(res+'\n')
   return


def check_if_name_exists(data, nu):
    s = nu.split('\t')
    for x in data['authors']:
        if x['name']==s[0] and x['university']==s[1]:
            return 0
    return 1

def check_if_coauthor_exists_or_add(data, nu, coauthor_name):
    s = nu.split('\t')
    for x in data['authors']:
        if x['name']==s[0] and x['university']==s[1]:
            for coauthor in x['coauthors']:
                if(coauthor == coauthor_name):
                    return 0
            x['coauthors'].append(coauthor_name)
    return 1

def adjust_coauthors(coauthors):
	res = []
	for e in coauthors:
		s = e.split('\t')
		res.append({'name': s[0], 'university':s[1]})
	return res

# def check_if_coauthor_exists(data, name, coauthor_name):
#     for x in data['authors']:
#         if x['name']==name:
#             x['coauthors'].append(coauthor_name)
#     return

# def take_name(l):
# 	res = []
# 	for i in l:
# 		j=i.split('\t')
# 		res.append(j[0])
# 	return res


# Temporary write the results in a file
# For each line we have one Swiss university with one or some memebers
# def write_in_file(text):
# 	res = "";
#    if 'Switzerland' in text:
#       file_result.write(text+'\n')
#    return


# FIRST PART: take all the necessary information and save them in a file
# Open the file with all html pages "apache-nutch-1.14/dump/dump"
file = open("apache-nutch-1.14/dump/dump","r")
# Read the file
content = file.read()


# Make the regex: we want to take all <dd> elements that can
# end with <dt> or </dl>
# re.MULTILINE|re.DOTALL allow to take multiline text
# regex = re.compile("<dd>(.*?)Switzerland(.*?)<dt>",  re.MULTILINE|re.DOTALL)
regex = re.compile("<dd>(.*?)((<dt>)|(</dl>))",  re.MULTILINE|re.DOTALL)

# find all matching strings with the regex
all_matching = re.findall(regex, content)
all_matching = [x[0] for x in all_matching]
# transform all matching strings in the format required
all_matching = map(to_plane_text, all_matching)

# Use this temporary file to store information
file_result = open("result.txt","w")
# Split the lines and write them in the file
map(split_lines, all_matching)

# close used files
file.close()
file_result.close()


# SECOND PART: take the information, extract a list of names
# with their universities
file_input = open("result.txt","r")
file_output = open("authors.json", "w")
content_input = file_input.read()
file_output.truncate()

# Take the lines of the file
res = content_input.split('\n')


data = {}
data['authors'] = []


# For each line we extract the names and the university,
# in one file we write the lists of names with their respective university
# in the other file we write the requests for Mendeley API
for y in res:
   parts = y.split(';')
   names = []
   for x in parts:
      x = re.split(', | and', x)
      x.remove(x[len(x)-1])
      for index in range(0,len(x)-1):
         name = re.sub(' +',' ',x[index].replace('and ', ' ')).rstrip().lstrip()
         university = re.sub(' +',' ',x[len(x)-1])
         nu = name + '\t' + university
         if (nu not in names):
            names.append(nu)
   for count in range(0,len(names)):
      coauthors = list(names)
      coauthors.remove(names[count])
      # coauthors = take_name(coauthors)
      if(check_if_name_exists(data, names[count])):
         s = names[count].split('\t')
         data['authors'].append({'name': s[0], 'university':s[1], 'coauthors': coauthors})
      else:
         for c in coauthors:
            check_if_coauthor_exists_or_add(data, names[count], c)


for elem in data['authors']:
   elem['coauthors'] = adjust_coauthors(elem['coauthors'])

json.dump(data, file_output)

file_input.close()
file_output.close()
# os.remove("result.txt")