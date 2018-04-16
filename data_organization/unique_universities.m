fname = '../information_retrieval/universities.json';
fid = fopen(fname);
raw = fread(fid,inf);
str = char(raw');
fclose(fid);
val = jsondecode(str);
val = struct2cell(val(1));
universities = val{1};
u = unique(universities);
