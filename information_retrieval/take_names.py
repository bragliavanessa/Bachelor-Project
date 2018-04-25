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
   fileLine = (re.sub(' +',' ', fileLine.replace('\t','').replace('<em>', '').replace('<EM>', '').replace('</em>', '').replace('</EM>', '').replace('<img src="../updated.gif" alt="updated">', '')))
   return fileLine


# Take only the Switzerland researchers and same them temporarily in a file
def split_lines(fileLine):
   if (not ((',</s>' not in fileLine) and (',</S>' not in fileLine) and ('</EM></s>' not in fileLine) and ('</em></s>' not in fileLine) and (not fileLine.endswith(',')))):
      return ""
   else:
      return fileLine.replace('</s>','').replace('</S>','')

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



def adjust_name(name):
   name = name.replace(',', '').replace(' and', '').replace('and ', '')
   return name


'''##############################
      END HELPER FUNCTIONS
################################# '''


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

# Split the lines and write them in the file
all_matching = map(split_lines, all_matching)

# close used files
file.close()


# SECOND PART: take the information, extract a list of names
# with their universities
file_output = open("authors.json", "w")
file_output.truncate()

data = {}
data['authors'] = []
data['authors_swiss'] = []

regex_universities = re.compile(",(.*?) and (.*?),")

uni_to_delete = [['German Aerospace Center (DLR)', ' Simulation'],
                 ['University of Tennessee', ' ORNL'],
                 ['University of California', ' Berkeley'],
                 ['Institute of Mathematics', ' Physics'],
                 ['University of California', ' Los Angeles - IPAM'],
                 ['Institut f\xc3\xbcr Numerische Simulation', ' Universit\xc3\xa4t Bonn'],
                 ['Chinese University of Hong Kong', ' Hong Kong'],
                 ['Indian Institute of Space', ' Science'],
                 ['Charles University', ' Prague;'],
                 ['University of California', ' Davis'],
                 ['Institut f\xc3\xbcr Numerische Simulation', ' Universit\xc3\xa4t Bonn'],
                 ['Khalifa University of Science', ' Technology'],
                 ['University of Wisconsin', ' Madison']]

# For each line we extract the names with relative universities,
# and we organized the results in a json file with a list of authors
# Each author has a name, a university and a list of coauthors
for y in all_matching:
   k = y.split('\n')
   k = filter(lambda x: x!="", k)
   if(len(k)>1):
      j =[]
      i=0
      l=[]
      for elem in k:
         if(';'in elem):
            l.append(elem)
            j.append(l)
            l=[]
         else:
            l.append(elem)
      if(l):
         j.append(l)
      names = []
      for elem in j:
         info = elem[len(elem)-1]
         elem.remove(elem[len(elem)-1])
         names_list = map(adjust_name, elem)
         multiple_uni = re.findall(regex_universities, info)
         if(multiple_uni):
            if((info.count(" and "))==1):
               info.replace(', and ', ' and ')
               unis = info.split(',')
               uni=[]
               universities = []
               for elem in unis:
                  if(' and ' not in elem):
                     uni.append(elem)
                  else:
                     uni.append(elem.split(' and ')[0])
                     uni = filter(lambda x: x!="", uni)
                     if(len(uni)==2) and (uni not in uni_to_delete):
                        universities.append(uni[0]+'\t'+uni[1])
                     uni = [elem.split(' and ')[1]]
               if(len(uni)==2)and (uni not in uni_to_delete):
                  universities.append(uni[0]+'\t'+uni[1])
            else:
               universities = []
         else:
            unis = info.split(',')
            if(len(unis)==1):
               universities = []
            elif(len(unis)==2):
               universities = []
               universities.append(unis[0]+'\t'+unis[1])
            elif(len(unis)==3):
               universities = []
               universities.append(unis[0]+','+unis[1]+'\t'+ unis[2])
            else:
               universities = []

         if(names_list and universities):
            # print universities
            for n in names_list:
               for u in universities:
                  nn = n+'\t'+u
                  if(nn not in names):
                     names.append(nn)

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
