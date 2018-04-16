take_name.py takes the crawled information and extract:

authors.json which contains a list of all authors
	Each author has the following fields:
	- name
	- university
	- list of coauthors
	Each coauthor has the following fields:
	- name
	- university

universities.json which contains a list of all universities (with duplicates)

names.json which contains a list of all authors
	Each author has the following fields:
	- name
	- university
	- index

edges.txt which contains all “edges” between coauthors.
	  Each line is like: (firstauthor_index,secondauthor_index)