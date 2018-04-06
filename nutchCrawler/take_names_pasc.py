import re
import os
import json
import sys


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


def adjust_coauthors(coauthors):
	res = []
	for e in coauthors:
		s = e.split('\t')
		res.append({'name': s[0], 'university':s[1]})
	return res

def take_names(co_organisers):
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


# FIRST PART: take all three html pages with a regex
# Open the file with all html pages "apache-nutch-1.14/dump2/dump"
file = open("apache-nutch-1.14/dump2/dump","r")
# Read the file
content = file.read()


# re.MULTILINE|re.DOTALL allow to take multiline text
regex = re.compile("<!DOCTYPE html(.*?)</html>",  re.MULTILINE|re.DOTALL)

# find all matching strings with the regex
all_matching = re.findall(regex, content)

print len(all_matching)
# <base href="http://www.pasc15.org/" />
# <base href="http://www.pasc16.org/" />

if(not (("<base href=\"http://www.pasc15.org/\" />" in all_matching[0]) and ("<base href=\"http://www.pasc16.org/\" />" in all_matching[1]))):
    sys.exit()

# <div class="tx-pascprogramm-pi1">(.*?)<!--Plugin inserted: [end]--></div>
# regex_pasc15 = re.compile("<div class=\"tx-pascprogramm-pi1\">(.*?)</div>",  re.MULTILINE|re.DOTALL)
regex_pasc15 = re.compile("<!-- new symposium(.*?)<!-- end symposium abstract",  re.MULTILINE|re.DOTALL)
programs = re.findall(regex_pasc15, all_matching[0])
programs2 = re.findall(regex_pasc15, all_matching[1])
programs = programs + programs2
# print len(programs)

data = {}
data['authors'] = []

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
	take_names(co_organisers)


for elem in data['authors']:
   elem['coauthors'] = adjust_coauthors(elem['coauthors'])


file_output = open("authors_new.json", "w")

json.dump(data, file_output)

file_output.close()
