# Lets use a regular expression to extract members' names
# from the crawled html pages
import re
import os

# Remove unnecessary content and excess spaces
def to_plane_text(fileLine):
   fileLine = (re.sub(' +',' ', fileLine.replace('\n', ' ').replace('\t',' ').replace("<em>", ' ').replace('</EM>', ' ').replace('</S>', ' ').replace('<img src="../updated.gif" alt="updated">', ' ')))
   return fileLine

# Split the lines per university
# The lines are organized such that the university with their memebers
# are separated by a ';'
def split_lines(fileLine):
   components = fileLine.split(';')
   map(write_in_file, components)
   return

# Temporary write the results in a file
# For each line we have one Swiss university with one or some memebers
def write_in_file(text):
   if 'Switzerland' in text:
      file_result.write(text+'\n')
   return


# CONSTANTS
# Token for Mendeley API requests
TOKEN = "MSwxNTIxMTIxOTQ1MzcxLDUxMDYwMzMzMSwxMDI4LGFsbCwsLDE2ZTZhNTE3NGRlNzAwNGUwODg4MWYxMGY1MWZlOTgzZTg3Y2d4cnFiLDJhOWM1NWE1LWY5NTYtMzJlMS1iYTU1LTA3NTAxYzRiYjI2NyxWMnlvYi0yYmx1YlpfOUc0aE1ETTZBM3Ridlk"
# Requests parts
REQUEST = "curl --request GET --header \"Authorization: Bearer "
REQUEST2 = "\" \"https://api.mendeley.com/catalog?query="
REQUEST3 = "&limit=100&view=bib\" > catalogs/catalog_"
REQUEST4 = ".json\n"


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
file_output = open("names.txt", "r+")
file_req = open("requests.sh", "w")
content_input = file_input.read()
file_output.truncate()
file_req.truncate()

# Take the lines of the file
res = content_input.split('\n')

# For each line we extract the names and the university,
# in one file we write the lists of names with their respective university
# in the other file we write the requests for Mendeley API
for x in res:
   x = re.split(', | and', x)
   x.remove(x[len(x)-1])
   for index in range(0, len(x)-1):
      name = (re.sub(' +',' ',x[index].replace('and ', ' ')).rstrip().lstrip()+'\t'+re.sub(' +',' ',x[len(x)-1]) +"\n")
      query_name = name.split('\t')[0].replace(' ', '+')
      file_name = name.split('\t')[0].replace(' ', '_')
      file_output.close()
      file_output = open("names.txt", "r+")
      content_output = file_output.read()
      if (name not in content_output):
         file_output.write(name)
         file_req.write(REQUEST + TOKEN + REQUEST2 + query_name + REQUEST3 + file_name + REQUEST4)

file_input.close()
file_output.close()
os.remove("result.txt")
