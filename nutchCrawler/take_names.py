# Lets use a regular expression to extract members' names
# from the crawled html pages
import re
import os
import json


'''##############################
         HELPER FUNCTIONS
################################# '''

# Remove unnecessary content and excess spaces
def to_plane_text(fileLine):
   fileLine = (re.sub(' +',' ', fileLine.replace('\n', ' ').replace('\t',' ').replace("<em>", ' ').replace('</EM>', ' ').replace('</S>', ' ').replace('<img src="../updated.gif" alt="updated">', ' ')))
   return fileLine


# Take only the Switzerland researchers and same them temporarily in a file
def split_lines(fileLine):
   components = fileLine.split(';')
   res = ""
   for x in components:
	   if 'Switzerland' in x:
		   res = res + x + ';';
   if res != "":
      file_result.write(res+'\n')
   return

# Extract names from pasc conferences
def take_names_pasc(co_organisers):
	for x in co_organisers:
		if "Switzerland" in x:
			information = x.split('(')
			name = information[0].rstrip().lstrip()
			name = re.sub(' +',' ',name)
			universities = information[1].split(';')
			for x in universities:
				university = x.split(',')[0].rstrip().lstrip()
				university = re.sub(' +',' ',university)
				nu = name + '\t' + university
				if (nu not in names):
					names.append(nu)

	for count in range(0,len(names)):
		coauthors = list(names)
		coauthors.remove(names[count])
		if(check_if_name_exists(data, names[count])):
			s = names[count].split('\t')
			data['authors'].append({'name': s[0], 'university':s[1], 'coauthors': coauthors})
		else:
			for c in coauthors:
				check_if_coauthor_exists_or_add(data, names[count], c)

	return

# Check if the name has been already saved
def check_if_name_exists(data, nu):
    s = nu.split('\t')
    for x in data['authors']:
        if x['name']==s[0] and x['university']==s[1]:
            return 0
    return 1

# If the name of the author is already present, check
# if there are some coauthors to add
def check_if_coauthor_exists_or_add(data, nu, coauthor_name):
    s = nu.split('\t')
    for x in data['authors']:
        if x['name']==s[0] and x['university']==s[1]:
            for coauthor in x['coauthors']:
                if(coauthor == coauthor_name):
                    return 0
            x['coauthors'].append(coauthor_name)
    return 1

# Organizes the coauthors list such that we have an array of :
# {'name': coauthor_name, 'university': coauthor_university}
def adjust_coauthors(coauthors):
	res = []
	for e in coauthors:
		s = e.split('\t')
		res.append({'name': s[0], 'university':s[1]})
	return res

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

'''##############################
      END HELPER FUNCTIONS
################################# '''



# FIRST PART: take all the necessary information and save them in a file
# Open the file with all html pages "apache-nutch-1.14/dump/dump"
file = open("apache-nutch-1.14/dump/dump","r")
# Read the file
content = file.read()


# Make the regex: we want to take all <dd> elements that can
# end with <dt> or </dl>
# re.MULTILINE|re.DOTALL allow to take multiline text
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


# For each line we extract the names with relative universities,
# and we organized the results in a json file with a list of authors
# Each author has a name, a university and a list of coauthors
for y in res:
   parts = y.split(';')
   parts = filter(None, parts)
   names = []
   for x in parts:
      y = re.split(',', x)
      y.remove(y[len(y)-1])
      university = re.sub(' +',' ',y[len(y)-1]).rstrip().lstrip()
      y.remove(y[len(y)-1])

      y = ",".join(y)

      y = re.split(', | and', y)
      # y.remove(y[len(y)-1])

      for index in range(0,len(y)):
         name = re.sub(' +',' ',y[index].replace('and ', ' ')).rstrip().lstrip()
         # university = re.sub(' +',' ',x[len(x)-1]).rstrip().lstrip()
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



# THIRD PART: take two html pages with a regex about pasc conferences
# Open the file with all html pages "apache-nutch-1.14/dump2/dump"
file = open("apache-nutch-1.14/dump2/dump","r")
# Read the file
content = file.read()


# re.MULTILINE|re.DOTALL allow to take multiline text
regex = re.compile("<!DOCTYPE html(.*?)</html>",  re.MULTILINE|re.DOTALL)

# find all matching strings with the regex
all_matching = re.findall(regex, content)


if(not (("<base href=\"http://www.pasc15.org/\" />" in all_matching[0]) and ("<base href=\"http://www.pasc16.org/\" />" in all_matching[1]))):
    sys.exit()

# <div class="tx-pascprogramm-pi1">(.*?)<!--Plugin inserted: [end]--></div>
# regex_pasc15 = re.compile("<div class=\"tx-pascprogramm-pi1\">(.*?)</div>",  re.MULTILINE|re.DOTALL)
regex_pasc15 = re.compile("<!-- new symposium(.*?)<!-- end symposium abstract",  re.MULTILINE|re.DOTALL)
programs = re.findall(regex_pasc15, all_matching[0])
programs2 = re.findall(regex_pasc15, all_matching[1])
programs = programs + programs2


for i in programs:
	names = []
	regex_organiser = re.compile("Organiser:</td>(.*?)<td>(.*?)</td>",  re.MULTILINE|re.DOTALL)
	regex_co_organiser = re.compile("Co-organiser:</td>(.*?)<td>(.*?)</td>",  re.MULTILINE|re.DOTALL)
	regex_table = re.compile("<!-- begin single abstract programm(.*?)</tr>",  re.MULTILINE|re.DOTALL)

	organiser = re.findall(regex_organiser, i)
	co_organisers = re.findall(regex_co_organiser, i)
	table = re.findall(regex_table, i)

	organiser = [x[1] for x in organiser][0]
	co_organisers = [x[1] for x in co_organisers][0]

	co_organisers = co_organisers.split(');')
	co_organisers.append(organiser)

	regex_elem = re.compile("</strong>,(.*?)\)",  re.MULTILINE|re.DOTALL)
	for y in table:
		elem = re.findall(regex_elem, y)[0]
		co_organisers.append(elem)
	take_names_pasc(co_organisers)



# FOURTH PART: adjust coauthors to save all in a file
for elem in data['authors']:
   elem['coauthors'] = adjust_coauthors(elem['coauthors'])

json.dump(data, file_output)

file_input.close()
file_output.close()
os.remove("result.txt")


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
