function T = degree_centrality(A,M)
authors = A(1,:);
degree = sum(M);

[degree,I] = sort(degree,'descend');
degree = degree-1;
degree(degree<0)=0;
authors = authors(I);

T = table(I',authors', degree');
T.Properties.VariableNames{'Var1'} = 'Index';
T.Properties.VariableNames{'Var2'} = 'Authors';
T.Properties.VariableNames{'Var3'} = 'Degree_Centrality';
end
