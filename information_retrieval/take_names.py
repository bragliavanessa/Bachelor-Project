# coding=utf-8

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
      if 'Switzerland and ' in x:
         res=x.split(' and ')[0]+';';
         break
      if 'University of Zurich and ETH Zurich' in x:
         res = x.split(' and ETH')[0]+',Switzerland;'
         res = res+x.split('University')[0]+'ETH Zürich,Switzerland;'
         break
      if 'ETH Zürich and Paul Scherrer Institute' in x:
         res = x.split(' and ')[0]+',Switzerland;'
         res = res+x.split(' ETH')[0]+' Paul Scherrer Institute,Switzerland;'
         break
      res = res + x + ';';
   if res != "":
      file_result.write(res+'\n')
   return

# Helper function that adjust names of university
def adjust_university(uni):
   uni = uni.replace('Zurich', 'Zürich')
   uni = uni.replace('Institut', 'Institute')
   uni = uni.replace('Institutee', 'Institute')
   uni = uni.replace('Berne', 'Bern')
   uni = uni.replace('Bernee', 'Bern')
   uni = uni.replace('Universität', 'University of')
   uni = uni.replace('Université de Genève', 'University of Geneva')
   uni = uni.replace('Philip Morris Int.','Philip Morris International R&D')
   uni = uni.replace('IBM Research - Zurich','IBM Research')
   uni = uni.replace('IBM Research - Zürich','IBM Research')
   uni = uni.replace('IBM Research-Zürich','IBM Research')
   uni = uni.replace('Univeristy', 'University')
   uni = uni.replace('Universite de', 'University of')
   uni = uni.replace('Eidgenössische Technische Hochschule','ETH')
   uni = uni.replace('École Polytechnique Fédérale de Lausanne','EPFL')
   uni = uni.replace('Università della Svizzera italiana', 'USI')
   uni = uni.replace('Università della Svizzera Italiana', 'USI')
   uni = uni.replace('University of Lugano','USI')
   uni = uni.replace('Centre','Center')
   uni = uni.replace('and ', ' ').rstrip().lstrip()
   if 'polytechnique f' in uni:
      uni = uni.replace('polytechnique f','Polytechnique F')
   return uni

# Extract names from pasc conferences and insert them in
# json data['authors']
def take_names_pasc(co_organisers):
   for x in co_organisers:
      if "Switzerland" in x:
         information = x.split('(')
         name = information[0].rstrip().lstrip()
         name = re.sub(' +',' ',name)
         information[1] = information[1].replace('Philip Morris International R&D','Philip Morris Int.')
         if('HES-SO' in information[1]):
            universities = information[1].split(',')
         elif ('Netherlands' in information[1]):
            universities = [information[1].split('&')[0]]
         else:
            universities = re.split(';|/|&|,', information[1]);
         for x in universities:
            if('Switzerland)' in x):
               break
            if('Switzerland' in x):
               continue
            university = x.split(',')[0].rstrip().lstrip()
            university = re.sub(' +',' ',university)
            university = adjust_university(university)
            nu = name + '\t' + university +'\tSwitzerland'
            if (nu not in names):
               names.append(nu)

   for count in range(0,len(names)):
      coauthors = list(names)
      coauthors.remove(names[count])
      if(check_if_name_exists(data, names[count])):
         s = names[count].split('\t')
         data['authors_swiss'].append({'name': s[0], 'university':s[1], 'nation':s[2], 'coauthors': coauthors})
      else:
         for c in coauthors:
            check_if_coauthor_exists_or_add(data, names[count], c)
   return

# Check if the name has been already saved in json data['authors']
# If not we save it
def check_if_name_exists(data, nu):
    s = nu.split('\t')
    for x in data['authors']:
        if x['name']==s[0] and x['university']==s[1] and x['nation']==s[2]:
            return 0
    for x in data['authors_swiss']:
        if x['name']==s[0] and x['university']==s[1] and x['nation']==s[2]:
            return 0
    return 1

def check_if_name_exists_with_nation(data, nu):
    s = nu.split('\t')
    for x in data:
        if x['name']==s[0] and x['university']==s[1] and x['nation']==s[2]:
            return 0
    return 1

def check_if_name_exists_no_nation(data, nu):
   s = nu.split('\t')
   for x in data:
      if x['name']==s[0] and x['university']==s[1]:
           return 0
   return 1

# If the name of the author is already present in json data['authors'],
# check if there are some coauthors to add
def check_if_coauthor_exists_or_add(data, nu, coauthor_name):
    s = nu.split('\t')
    for x in data['authors']:
        if x['name']==s[0] and x['university']==s[1] and x['nation']==s[2]:
            for coauthor in x['coauthors']:
                if(coauthor == coauthor_name):
                    return 0
            x['coauthors'].append(coauthor_name)
    for x in data['authors_swiss']:
        if x['name']==s[0] and x['university']==s[1] and x['nation']==s[2]:
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
		res.append({'name': s[0], 'university':s[1], 'nation':s[2]})
	return res

# If the author is already in author_names['authors']
# take its index
def take_index(data, nu):
    s = nu.split('\t')
    for count in range(0,len(data)):
        if data[count]['name']==s[0] and data[count]['university']==s[1]:
            return count+1
    return -1

# Write in the edges file all the connection between authors
# such as (first_author_index,second_author_index)
def make_edges(id, ids, file):
   for i in ids:
      if(id != i):
         file.write('('+str(id)+','+str(i)+')\n')

'''##############################
      END HELPER FUNCTIONS
################################# '''

# uni_to_delete = ['1QBit','3M','A*STAR','www.charlesperry.com','and Adele Tortorici','eBay Research Labs','Yahoo! Research','Yahoo! Labs','Yahoo! Inc.','Yahoo Japan Corporation','Xilinx',
#                  'Xuefei Sexton','Wuxi','WorldQuant Research','Wilmington','William Knottenbelt','Wells Fargo','Wellcome Trust Center for Neuroimaging','Wei Ji Ma','Weapons Division',
#                  'Wallis Consulting','Wachovia Investments','Volvo Group Trucks Technology','Volkswagen','Vmware Research','Vigo']

# FIRST PART: take all the necessary information and save them in a file
# Open the file with all html pages "apache-nutch-1.14/dump/dump"
file = open("../nutch_crawler/apache-nutch-1.14/dump/dump","r")
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
data['authors_swiss'] = []


# For each line we extract the names with relative universities,
# and we organized the results in a json file with a list of authors
# Each author has a name, a university and a list of coauthors
for y in res:
   parts = y.split(';')
   parts = filter(None, parts)
   names = []
   for x in parts:
      j = re.split(',', x)
      if (len(j)>=3):
         nation = re.sub(' +',' ',j[len(j)-1]).rstrip().lstrip()
         j.remove(j[len(j)-1])
         university = re.sub(' +',' ',j[len(j)-1]).rstrip().lstrip()
         university = adjust_university(university)
         j.remove(j[len(j)-1])

         j = ",".join(j)

         j = re.split(', | and', j)

         for index in range(0,len(j)):
            if(nation=='</s>'):
               break
            name = re.sub(' +',' ',j[index].replace('and ', ' ')).rstrip().lstrip()
            nu = name + '\t' + university + '\t'+nation
            if (nu not in names):
               names.append(nu)
   for count in range(0,len(names)):
      coauthors = list(names)
      coauthors.remove(names[count])
      if(check_if_name_exists(data, names[count])):
         s = names[count].split('\t')
         if ('Switzerland' in s[2]):
            data['authors_swiss'].append({'name': s[0], 'university':s[1], 'nation':s[2], 'coauthors': coauthors})
         else:
            data['authors'].append({'name': s[0], 'university':s[1], 'nation':s[2], 'coauthors': coauthors})
      else:
         for c in coauthors:
            check_if_coauthor_exists_or_add(data, names[count], c)


# THIRD PART: take two html pages with a regex about pasc conferences
# Open the file with all html pages "apache-nutch-1.14/dump2/dump"
file = open("../nutch_crawler/apache-nutch-1.14/dump2/dump","r")
# Read the file
content = file.read()


# re.MULTILINE|re.DOTALL allow to take multiline text
regex = re.compile("<!DOCTYPE html(.*?)</html>",  re.MULTILINE|re.DOTALL)

# find all matching strings with the regex
all_matching = re.findall(regex, content)


if(not (("<base href=\"http://www.pasc15.org/\" />" in all_matching[0]) and ("<base href=\"http://www.pasc16.org/\" />" in all_matching[1]))):
    sys.exit()

# Regex for pasc conferences
regex_pasc = re.compile("<!-- new symposium(.*?)<!-- end symposium abstract",  re.MULTILINE|re.DOTALL)
programs = re.findall(regex_pasc, all_matching[0])
programs2 = re.findall(regex_pasc, all_matching[1])
programs = programs + programs2

# Take all the names from pasc conferences' pages
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
for elem in data['authors_swiss']:
   elem['coauthors'] = adjust_coauthors(elem['coauthors'])


# Save all in the output file
json.dump(data, file_output)

file_input.close()
file_output.close()
os.remove("result.txt")


# FIFTH PART: take the information in the json file and create a file
# containing the "edges" between coauthors

file_json = open('authors.json')
data_json = json.load(file_json)
swiss_information = open("swiss_information.json", "w")
edges_swiss = open("edges_swiss.txt", "w")
world_information = open("world_information.json", "w")
edges_world = open("edges_world.txt", "w")

author_indexes_swiss=[]
author_indexes=[]

information = {}
information['authors_swiss'] = []
information['universities_swiss'] = []
information['authors'] = []
information['universities'] = []
index = 1;

# Edges for swiss
for idx in range(0,len(data_json['authors_swiss'])):
   name = data_json['authors_swiss'][idx]['name']
   university = data_json['authors_swiss'][idx]['university']
   nu = name+'\t'+university

   if(check_if_name_exists_no_nation(information['authors_swiss'], nu)):
      information['authors_swiss'].append({'index': index, 'name': name, 'university': university})
      information['universities_swiss'].append(university)
      author_id = index
      index = index+1
   else:
      for x in information['authors_swiss']:
          if x['name']==name and x['university']==university:
              author_id = x['index']

   author_indexes_swiss.append(author_id)
   coauthor_indexes = []
   for author in data_json['authors_swiss'][idx]['coauthors']:
      if(author['nation']=='Switzerland'):
         nn = author['name']+'\t'+author['university']
         if(check_if_name_exists_no_nation(information['authors_swiss'], nn)):
            information['authors_swiss'].append({'index': index, 'name': author['name'], 'university': author['university']})
            information['universities_swiss'].append(author['university'])
            coauthor_indexes.append(index)
            index = index+1
         else:
            id = take_index(information['authors_swiss'], nn)
            if(id not in author_indexes_swiss):
               coauthor_indexes.append(id)

   make_edges(author_id, coauthor_indexes, edges_swiss)

# Edges from all the world
all_names = data_json['authors_swiss']+data_json['authors']
index = 1;

for idx in range(0,len(all_names)):
   name = all_names[idx]['name']
   university = all_names[idx]['university']
   nation = all_names[idx]['nation']
   nu = name+'\t'+university+'\t'+nation

   if(check_if_name_exists_with_nation(information['authors'], nu)):
      information['authors'].append({'index': index, 'name': name, 'university': university, 'nation': nation})
      information['universities'].append(university)
      author_id = index
      index = index+1
   else:
      for x in information['authors']:
          if x['name']==name and x['university']==university and x['nation']==nation:
              author_id = x['index']

   author_indexes.append(author_id)
   coauthor_indexes = []
   for author in all_names[idx]['coauthors']:
      nn = author['name']+'\t'+author['university']+'\t'+author['nation']
      if(check_if_name_exists_with_nation(information['authors'], nn)):
         information['authors'].append({'index': index, 'name': author['name'], 'university': author['university'], 'nation': author['nation']})
         information['universities'].append(author['university'])
         coauthor_indexes.append(index)
         index = index+1
      else:
         id = take_index(information['authors'], nn)
         if(id not in author_indexes):
            coauthor_indexes.append(id)

   make_edges(author_id, coauthor_indexes, edges_world)


swiss_file = {'names':information['authors_swiss'],'universities':information['universities_swiss']}
json.dump(swiss_file, swiss_information)

world_file = {'names':information['authors'],'universities':information['universities']}
json.dump(world_file, world_information)

file_json.close()
swiss_information.close()
edges_swiss.close()
world_information.close()
edges_world.close()
