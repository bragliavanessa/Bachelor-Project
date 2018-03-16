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
