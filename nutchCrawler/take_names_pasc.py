import re
import os
import json
import sys

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
regex_pasc15 = re.compile("<!-- new symposium(.*?)</table>",  re.MULTILINE|re.DOTALL)
programs = re.findall(regex_pasc15, all_matching[0])
print len(programs)

for i in programs:
    if("<td style=\"white-space: nowrap\">Organiser:</td>" not in i):
        sys.exit()

print "ALL"
