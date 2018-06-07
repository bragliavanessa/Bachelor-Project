
f = fopen('UNI.gexf', 'w');

fprintf(f, '<?xml version="1.0" encoding="UTF-8"?>\n');
fprintf(f, '<gexf xmlns:viz="http:///www.gexf.net/1.1draft/viz" version="1.1" xmlns="http://www.gexf.net/1.1draft">\n');
fprintf(f, '<graph defaultedgetype="undirected" idtype="string" type="static">\n');

u = triu(U) - diag(diag(U));

cm = [157,49,155;
137,42,151;
116,36,147;
96,30,143;
76,24,139;
56,17,135;
35,11,131;
15,5,127;
0,4,128;
0,20,145;
0,36,162;
0,52,179;
0,68,196;
0,84,213;
0,100,230;
0,116,247;
8,132,255;
24,149,255;
40,166,255;
56,183,255;
72,200,255;
88,217,255;
104,234,255;
120,251,255;
136,255,243;
153,255,226;
170,255,210;
187,255,194;
204,255,177;
221,255,161;
238,255,145;
255,255,128];

index = [7 8 25 12 20 30 24 11 31 4 19 21 27 6 29 5 26 23 22 18 28 2 15 1 3 9 16 10 13 14 17 32];
sz    = length(index):-1:1;

fprintf(f, '<nodes count="%d">\n', size(u,1));
for j = 1:size(u,1)
    k = index(j);
    fprintf(f, '<node id="%.1f" label="%s"> ', k, univ{k});
    fprintf(f, '<viz:color r="%d" g="%d" b="%d"/> ', cm(k,1), cm(k,2), cm(k,3));
    fprintf(f, '<viz:size value="%d"/>', sz(k));
    fprintf(f, '</node>\n');
end
fprintf(f, '</nodes>\n');

fprintf(f, '<edges count="%d">\n', nnz(u));
e = 1;
for k = 1:size(u,1)
    I = find(u(k,:));
    for j = I
        fprintf(f, '<edge id="%d" source="%.1f" target="%.1f"/>\n', e, k, j);
        e = e+1;
    end
end
fprintf(f, '</edges>\n');
fprintf(f, '</graph>\n');
fprintf(f, '</gexf>\n');
fclose(f);
