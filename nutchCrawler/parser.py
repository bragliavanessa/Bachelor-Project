# Lets use a regular expression to extract members' names
# from the crawled html pages
import re
from operator import methodcaller

def to_plane_text(fileLine):
   fileLine = (re.sub(' +',' ', fileLine.replace('\n', ' ').replace('\t',' ').replace("<em>", ' ').replace('</EM>', ' ').replace('</S>', ' ').replace('<img src="../updated.gif" alt="updated">', ' ')))
   return fileLine

def split_lines(fileLine):
   components = fileLine.split(';')
   map(write_in_file, components)
   return

def write_in_file(text):
   if 'Switzerland' in text:
      file_result.write(text+'\n')
   return


# Open the file with all html pages "apache-nutch-1.14/dump/dump"
file = open("apache-nutch-1.14/dump/dump","r")
# file = open("prova.txt","r")

# Read the file
content = file.read()

# Make the regex: we want to take all <dd> elements that can
# end with <dt> or </dl>
# re.MULTILINE|re.DOTALL allow to take multiline text
# regex = re.compile("<dd>(.*?)Switzerland(.*?)<dt>",  re.MULTILINE|re.DOTALL)
regex = re.compile("<dd>(.*?)((<dt>)|(</dl>))",  re.MULTILINE|re.DOTALL)


all_matching = re.findall(regex, content)
all_matching = [x[0] for x in all_matching]
all_matching = map(to_plane_text, all_matching)

# print all_matching
# print len(all_matching)

file_result = open("result.txt","w")

map(split_lines, all_matching)

file.close()
file_result.close()

file_input = open("result.txt","r")
file_output = open("names.txt", "r+")
content_input = file_input.read()


res = content_input.split('\n')


for x in res:
   print x
   x = re.split(', | and', x)
   print x
   x.remove(x[len(x)-1])
   for index in range(0, len(x)-1):
      name = (re.sub(' +',' ',x[index].replace('and ', ' ')).rstrip().lstrip()+'\t'+re.sub(' +',' ',x[len(x)-1]) +"\n")
      file_output.close()
      file_output = open("names.txt", "r+")
      content_output = file_output.read()
      if (name not in content_output):
         file_output.write(name)

file_input.close()
file_output.close()
