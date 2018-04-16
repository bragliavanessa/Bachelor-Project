% Take all the "edges" saved in the file "edges.txt"
fname = '../information_retrieval/edges.txt';
fid = fopen(fname);
raw = fread(fid,inf);
str = char(raw');
fclose(fid);
couples = strsplit(str, '\n');


% Take the number of authors we have to set the matrix
fname_names = '../information_retrieval/names.json';
fid_names = fopen(fname_names);
raw_names = fread(fid_names,inf);
str_names = char(raw_names');
fclose(fid_names);
val = jsondecode(str_names);
val = struct2cell(val(1));
authors = val{1};
n = size(authors,1);

% Takes universities array, without duplicates
fname = '../information_retrieval/universities.json';
fid = fopen(fname);
raw = fread(fid,inf);
str = char(raw');
fclose(fid);
val = jsondecode(str);
val = struct2cell(val(1));
universities = val{1};
univ = unique(universities);
uni_size = size(univ,1);

M = zeros(n,n);
for i = 1:n
    M(i,i)=1;
end

U = zeros(uni_size,uni_size);
W = zeros(uni_size,uni_size);

% Create the matrix and where there is an "edge" put a 1 in
% matrix entry, otherwise leave 0s
for i = 1:numel(couples)
    if(couples{i})
        elem = couples{i};
        elem = strsplit(elem, ',');
        elemx = elem{1,1};
        elemy = elem{1,2};
        x = strsplit(elemx, '(');
        x = str2double(x{1,2});
        y = strsplit(elemy, ')');
        y = str2double(y{1,1});
        M(x,y)=1;
        M(y,x)=1;
        uni1 = authors(x).('university');
        index_uni1 = find(strcmp(univ,uni1));
        uni2 = authors(y).('university');
        index_uni2 = find(strcmp(univ,uni2));
        U(index_uni1,index_uni2)=1;
        U(index_uni2,index_uni1)=1;
        W(index_uni1,index_uni2)= W(index_uni1,index_uni2)+1;
        W(index_uni2,index_uni1)= W(index_uni1,index_uni2)+1;
    end
end
