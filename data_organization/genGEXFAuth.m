
f = fopen('AUTH.gexf', 'w');

fprintf(f, '<?xml version="1.0" encoding="UTF-8"?>\n');
fprintf(f, '<gexf xmlns:viz="http:///www.gexf.net/1.1draft/viz" version="1.1" xmlns="http://www.gexf.net/1.1draft">\n');
fprintf(f, '<graph defaultedgetype="undirected" idtype="string" type="static">\n');

m = triu(M) - diag(diag(M));

cm = [157,49,155;
154,48,155;
152,47,154;
149,46,154;
147,46,153;
145,45,153;
142,44,152;
140,43,152;
137,43,151;
135,42,151;
132,41,150;
130,40,150;
127,40,149;
125,39,149;
122,38,148;
120,37,148;
117,36,147;
115,36,147;
113,35,146;
110,34,146;
108,33,145;
105,33,145;
103,32,144;
100,31,144;
98,30,143;
95,30,143;
93,29,142;
90,28,142;
88,27,141;
86,27,141;
83,26,140;
81,25,140;
78,24,139;
76,23,139;
73,23,138;
71,22,138;
68,21,137;
66,20,137;
63,20,136;
61,19,136;
58,18,135;
56,17,135;
54,17,134;
51,16,134;
49,15,133;
46,14,133;
44,14,132;
41,13,132;
39,12,131;
36,11,131;
34,11,130;
31,10,130;
29,9,129;
26,8,129;
24,7,128;
22,7,128;
19,6,127;
17,5,127;
14,4,126;
12,4,126;
9,3,126;
7,2,125;
4,1,125;
2,1,124;
0,0,124;
0,2,126;
0,4,128;
0,6,130;
0,8,132;
0,10,134;
0,12,137;
0,14,139;
0,16,141;
0,18,143;
0,20,145;
0,22,147;
0,24,149;
0,26,151;
0,28,153;
0,30,155;
0,32,157;
0,33,159;
0,35,161;
0,37,163;
0,39,165;
0,41,167;
0,43,169;
0,45,172;
0,47,174;
0,49,176;
0,51,178;
0,53,180;
0,55,182;
0,57,184;
0,59,186;
0,61,188;
0,63,190;
0,64,192;
0,66,194;
0,68,196;
0,70,198;
0,72,200;
0,74,202;
0,76,205;
0,78,207;
0,80,209;
0,82,211;
0,84,213;
0,86,215;
0,88,217;
0,90,219;
0,92,221;
0,94,223;
0,96,225;
0,97,227;
0,99,229;
0,101,231;
0,103,233;
0,105,235;
0,107,237;
0,109,240;
0,111,242;
0,113,244;
0,115,246;
0,117,248;
0,119,250;
0,121,252;
0,123,254;
1,125,255;
3,127,255;
5,129,255;
7,131,255;
9,133,255;
11,135,255;
13,137,255;
15,139,255;
16,141,255;
18,143,255;
20,145,255;
22,147,255;
24,149,255;
26,151,255;
28,154,255;
30,156,255;
32,158,255;
34,160,255;
36,162,255;
38,164,255;
40,166,255;
42,168,255;
44,170,255;
46,172,255;
48,174,255;
49,176,255;
51,178,255;
53,180,255;
55,182,255;
57,184,255;
59,186,255;
61,189,255;
63,191,255;
65,193,255;
67,195,255;
69,197,255;
71,199,255;
73,201,255;
75,203,255;
77,205,255;
79,207,255;
80,209,255;
82,211,255;
84,213,255;
86,215,255;
88,217,255;
90,219,255;
92,222,255;
94,224,255;
96,226,255;
98,228,255;
100,230,255;
102,232,255;
104,234,255;
106,236,255;
108,238,255;
110,240,255;
112,242,255;
113,244,255;
115,246,255;
117,248,255;
119,250,255;
121,252,255;
123,254,255;
125,255,254;
127,255,252;
129,255,250;
131,255,248;
133,255,246;
135,255,244;
138,255,242;
140,255,240;
142,255,238;
144,255,236;
146,255,234;
148,255,232;
150,255,230;
152,255,228;
154,255,226;
156,255,224;
158,255,222;
160,255,220;
162,255,218;
164,255,216;
166,255,214;
168,255,212;
171,255,210;
173,255,208;
175,255,206;
177,255,204;
179,255,202;
181,255,200;
183,255,198;
185,255,196;
187,255,194;
189,255,192;
191,255,190;
193,255,188;
195,255,186;
197,255,184;
199,255,182;
201,255,180;
203,255,178;
206,255,176;
208,255,174;
210,255,172;
212,255,170;
214,255,168;
216,255,166;
218,255,164;
220,255,162;
222,255,160;
224,255,158;
226,255,156;
228,255,154;
230,255,152;
232,255,150;
234,255,148;
236,255,146;
239,255,144;
241,255,142;
243,255,140;
245,255,138;
247,255,136;
249,255,134;
251,255,132;
253,255,130;
255,255,128];

index = [12 31 57 4 164 24 87 55 38 1 ...
213 161 73 90 262 308 83 119 61 320 ...
311 328 314 48 81 95 208 290 321 342 ...
54 52 151 46 195 43 42 191 192 62 ...
53 144 382 383 63 120 21 14 70 71 ...
72 69 378 379 149 153 150 152 170 169 ...
171 344 345 346 44 45 194 196 355 77 ...
79 75 76 78 80 387 389 391 393 388 ...
390 392 99 100 122 123 130 131 132 147 ...
148 155 156 158 159 177 178 179 189 190 ...
204 205 217 218 219 220 221 222 226 227 ...
228 229 230 232 233 234 238 239 240 241 ...
242 252 253 254 255 256 258 259 271 272 ...
273 274 275 276 280 281 282 299 300 301 ...
302 304 305 306 352 353 354 368 369 370 ...
394 395 396 68 128 129 136 137 224 225 ...
245 247 372 374 376 398 400 246 248 323 ...
324 325 326 327 371 373 375 377 399 401 ...
249 250 251 332 329 330 331 334 335 333 ...
336 49 50 175 176 91 92 88 365 366 ...
364 367 109 110 111 319 318 317 23 385 ...
386 348 350 349 351 25 312 313 17 15 ...
16 337 18 84 85 267 269 8 9 113 ...
115 116 114 361 210 211 212 362 363 381 ...
165 163 186 187 184 185 180 181 182 183 ...
291 96 97 207 209 289 33 32 141 142 ...
34 35 309 310 118 315 316 160 322 20 ...
22 29 28 107 105 106 104 338 143 145 ...
263 264 265 202 203 384 3 356 268 358 ...
359 5 58 59 380 41 193 51 82 357 ...
93 94 27 26 86 112 117 125 168 166 ...
167 343 37 140 146 36 360 103 108 102 ...
2 6 7 303 154 47 197 214 56 89 ...
60 19 13 11 30 10 39 40 64 65 ...
66 67 74 98 101 121 124 126 127 133 ...
134 135 138 139 157 162 172 173 174 188 ...
198 199 200 201 206 215 216 223 231 235 ...
236 237 243 244 257 260 261 266 270 277 ...
278 279 283 284 285 286 287 288 292 293 ...
294 295 296 297 298 307 339 340 341 347 ...
397 402];
sz    = length(index):-1:1;

mn = min(TP.Pagerank);
h  = (max(TP.Pagerank) - mn) / 255;
%mp = min(TP.Pagerank):h:max(TP.Pagerank);

fprintf(f, '<nodes count="%d">\n', size(m,1));
for j = 1:size(m,1)
    k = index(j);
    kcm = floor((TP.Pagerank(j)-mn)/h + 1);
    a = authors(k).name;
    fprintf(f, '<node id="%.1f" label="%s"> ', k, a);
    fprintf(f, '<viz:color r="%d" g="%d" b="%d"/> ', cm(kcm,1), cm(kcm,2), cm(kcm,3));
    fprintf(f, '<viz:size value="%d"/>', sz(j));
    fprintf(f, '</node>\n');
end
fprintf(f, '</nodes>\n');

fprintf(f, '<edges count="%d">\n', nnz(m));
e = 1;
for k = 1:size(m,1)
    I = find(m(k,:));
    for j = I
        fprintf(f, '<edge id="%d" source="%.1f" target="%.1f"/>\n', e, k, j);
        e = e+1;
    end
end
fprintf(f, '</edges>\n');
fprintf(f, '</graph>\n');
fprintf(f, '</gexf>\n');
fclose(f);
