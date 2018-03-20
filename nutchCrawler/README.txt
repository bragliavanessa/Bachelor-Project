take_name.py takes the crawled information and extract a json file with a list of authors.
Each author has the following fields:
- name
- university
- list of coauthors
Each coauthor has the following fields:
- name
- university

take_edges.py takes the file produced by take_name.py and write:
- a file with a list of all authors (index, name, author) --> names.json
- a file with all edges (author_index, coauthor_index) --> edges.txt

create_matrix.m take information from edges.txt and organizes the information
in a matrix
