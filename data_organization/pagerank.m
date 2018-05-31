function T = pagerank(U,G,p)
% PAGERANK  Google's PageRank
% pagerank(U,G,p) uses the list of authors U and adjacency matrix G,
% together with a damping factory p, to compute and plot
% a bar graph of page rank, and print the first 15 most "famous" authors.

% Eliminate any self-referential collaborations
G = G - diag(diag(G));
  
% c = out-degree, r = in-degree
[~,n] = size(G);
c = sum(G,1);
r = sum(G,2);

% Scale column sums to be 1 (or 0 where there are no out links).
k = find(c~=0);
D = sparse(k,k,1./c(k),n,n);

% Solve (I - p*G*D)*x = e
e = ones(n,1);
I = speye(n,n);
x = (I - p*G*D)\e;

% Normalize so that sum(x) == 1.
x = x/sum(x);

% Bar graph of page rank.
figure
shg
bar(x)
x

title('Page Rank')
xlim([1, length(x)]);


[~,q] = sort(-x);
k = 1;
indexes=[];
pagerank=[];
in=[];
out=[];
name=[];
university=[];
if isstruct(U)
    while (k <= n)
        j = q(k);
        temp1  = r(j);
        temp2  = c(j);
        indexes = [indexes j];
        pagerank = [pagerank x(j)];
        in = [in full(temp1)];
        out = [out full(temp2)];
        name = [name {U(j).('name')}];
        university = [university {U(j).('university')}];
        k = k+1;
    end
    T = table(indexes', pagerank', in', out', name', university');
    T.Properties.VariableNames{'Var1'} = 'Index';
    T.Properties.VariableNames{'Var2'} = 'Pagerank';
    T.Properties.VariableNames{'Var3'} = 'In_degree';
    T.Properties.VariableNames{'Var4'} = 'Out_degree';
    T.Properties.VariableNames{'Var5'} = 'Name';
    T.Properties.VariableNames{'Var6'} = 'University';
else
    while (k <= n)
        j = q(k);
        temp1  = r(j);
        temp2  = c(j);
        indexes = [indexes j];
        pagerank = [pagerank x(j)];
        in = [in full(temp1)];
        out = [out full(temp2)];
        university = [university U(j)];
        k = k+1;
    end
    T = table(indexes', pagerank', in', out', university');
    T.Properties.VariableNames{'Var1'} = 'Index';
    T.Properties.VariableNames{'Var2'} = 'Pagerank';
    T.Properties.VariableNames{'Var3'} = 'In_degree';
    T.Properties.VariableNames{'Var4'} = 'Out_degree';
    T.Properties.VariableNames{'Var5'} = 'University';
end
end

