fname = 'edges.txt';
fid = fopen(fname);
raw = fread(fid,inf);
str = char(raw');
fclose(fid);
couples = strsplit(str, '\n');

% Da recuperare quanti nomi sono
% per initializzare la matrice
n=253;
m = zeros(n,n);


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
