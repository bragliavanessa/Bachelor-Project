% Take all the "edges" saved in the file "edges_swiss.txt"
% Edges relative only to Swiss authors
fname = '../information_retrieval/edges_swiss.txt';
fid = fopen(fname);
raw = fread(fid,inf);
raw = char(raw');
fclose(fid);
couples = strsplit(raw, '\n');

% Take all the "edges" saved in the file "edges_world.txt"
fname = '../information_retrieval/edges_world.txt';
fid = fopen(fname);
raw = fread(fid,inf);
raw = char(raw');
fclose(fid);
couples_world = strsplit(raw, '\n');


% Take the number of authors we have to set the matrix
% Only Swiss
fname_names = '../information_retrieval/swiss_information.json';
fid_names = fopen(fname_names);
raw = fread(fid_names,inf);
raw = char(raw');
fclose(fid_names);
val = jsondecode(raw);
val = struct2cell(val(1));
authors = val{2};
n = size(authors,1);
A = {};
for a=1:n
    A{end+1} = authors(a).('name');
end

% Takes universities array, without duplicates
% Only Swiss
universities = val{1};
univ = unique(universities);
uni_size = size(univ,1);

% Take the number of authors we have to set the matrix
fname_names = '../information_retrieval/world_information.json';
fid_names = fopen(fname_names);
raw = fread(fid_names,inf);
raw = char(raw');
fclose(fid_names);
val = jsondecode(raw);
val = struct2cell(val(1));
authors_world = val{2};
n_world = size(authors_world,1);

% Takes universities array, without duplicates
universities_world = val{1};
univ_world = unique(universities_world);
uni_world_size = size(univ_world,1);


% Create Swiss matrices
% Authors matrix with 'coauthorship' (M)
% Universities matrix (weighted (W) and not (U))
M = zeros(n,n);
U = zeros(uni_size,uni_size);
W = zeros(uni_size,uni_size);

for i = 1:n
    M(i,i)=1;
    if(i<=uni_size)
        U(i,i)=1;
        W(i,i)=1;
    end
end

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

% Create world matrices
% Authors matrix with 'coauthorship' (MW)
% Universities matrix (weighted (WW) and not (UW))
MW = zeros(n_world,n_world);
UW = zeros(uni_world_size,uni_world_size);
WW = zeros(uni_world_size,uni_world_size);

for i = 1:n_world
    MW(i,i)=1;
    if(i<=uni_world_size)
        UW(i,i)=1;
        WW(i,i)=1;
    end
end

% Create the matrix and where there is an "edge" put a 1 in
% matrix entry, otherwise leave 0s
for i = 1:numel(couples_world)
    if(couples_world{i})
        elem = couples_world{i};
        elem = strsplit(elem, ',');
        elemx = elem{1,1};
        elemy = elem{1,2};
        x = strsplit(elemx, '(');
        x = str2double(x{1,2});
        y = strsplit(elemy, ')');
        y = str2double(y{1,1});
        MW(x,y)=1;
        MW(y,x)=1;
        uni1 = authors_world(x).('university');
        index_uni1 = find(strcmp(univ_world,uni1));
        uni2 = authors_world(y).('university');
        index_uni2 = find(strcmp(univ_world,uni2));
        UW(index_uni1,index_uni2)=1;
        UW(index_uni2,index_uni1)=1;
        WW(index_uni1,index_uni2)= WW(index_uni1,index_uni2)+1;
        WW(index_uni2,index_uni1)= WW(index_uni1,index_uni2)+1;
    end
end
