
f = fopen('UNI.dot', 'w');

fprintf(f, 'graph{\n');

u = triu(U) - diag(diag(U));

for k = 1:size(u,1)
    I = find(u(k,:));
    for j = I
        %fprintf(f, '\t%s -- %s;\n', univ{k}, univ{j});
        fprintf(f, '\t%d -- %d;\n', k, j);
    end
end

fprintf(f, '}\n');

fclose(f);