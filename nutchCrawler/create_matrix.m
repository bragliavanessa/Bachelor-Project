% Take all the "edges" saved in the file "edges.txt"
fname = 'edges.txt';
fid = fopen(fname);
raw = fread(fid,inf);
str = char(raw');
fclose(fid);
couples = strsplit(str, '\n');


% Take the number of authors we have to set the matrix
fname_names = 'names.json';
fid_names = fopen(fname_names);
raw_names = fread(fid_names,inf);
str_names = char(raw_names');
fclose(fid_names);
val = jsondecode(str_names);
val = struct2cell(val(1));
authors = val{1};
n = size(authors,1);


m = zeros(n,n);
for i = 1:n
    m(i,i)=1;
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
        m(x,y)=1;
        m(y,x)=1;
    end
end
