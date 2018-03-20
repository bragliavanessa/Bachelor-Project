# coding=utf-8

def check_if_name_exists(data, name):
    for x in data['authors']:
        if x['name']==name:
            print 1
            return 1
    print 0
    return 0

def check_if_coauthor_exists(data, name, coauthor_name):
    for x in data['authors']:
        if x['name']==name:
            for coauthor in x['coauthors']:
                if(coauthor == coauthor_name):
                    print 1
                    return 1
    print 0
    return 0

data = {}
data['authors'] = []

data['authors'].append({'name' : 'Giuseppa', 'coauthors': ["Filippo", 'Giuseppe']})

if (not check_if_name_exists(data, "Giuseppa")):
    print "ciao"
check_if_name_exists(data, "Filippo")
check_if_coauthor_exists(data, "Giuseppa", "Filippo")
check_if_coauthor_exists(data, "Giuseppa", "Giancarlo")


def take_name(l):
	res = []
	for i in l:
		j=i.split('\t')
		res.append(j[0])
	return res

name1 = 'Giuseppe\tUniversitá'
name2 = 'fig\tUniverstá'
name3 = 'ggigiig\tUnisitá'
list = [name1, name2, name3]
print list
list = take_name(list)
print list


def adjust_coauthors(coauthors):
	res = []
	for e in coauthors:
		s = e.split('\t')
		res.append({'name': s[0], 'university':s[1]})
	return res

name1 = 'Giuseppe\tUniversitá'
name2 = 'fig\tUniverstá'
name3 = 'ggigiig\tUnisitá'
list = [name1, name2, name3]

list = adjust_coauthors(list)
print list
