%% Matrix visualization
figure
spy(M)
title('authors adjacency matrix')

figure
imagesc(W)
colorbar
title('universities adjacency matrix')
%% PageRank
% Call the function with swiss authors' information
TP = pagerank(authors,M,0.85);
% Display the first 15 auhtors of the ranking
TP(1:15,:)

%% Degree Centrality
% Rank authors only considering only number of collaboration and not
% quality
TD = degree_centrality(A,M);
TD(1:10,:)


%% The Reverse Cuthill McKee Ordering
r = symrcm(M(2:end, 2:end));
prcm= [1 r+1];
figure
subplot(1,2,1)
spy(M);
title('Default connectivity matrix')
subplot(1,2,2)
spy(M(prcm,prcm))
title('Ordered connectivity matrix')

% Matrix sparsity = 0.0073
sparsity = nnz(M)/numel(M);
%% Spectral graph Partitioning
itr = 0;
k = 4;
[g1,g2] = spectral_partitioning(M);

while(k/2>1)
    [g3,g4] = spectral_partitioning(M(g1,g1));
    [g5,g6] = spectral_partitioning(M(g2,g2));
    k = k/2;
end


group1 = authors(g1(g3));
group2 = authors(g1(g4));
group3 = authors(g2(g5));
group4 = authors(g2(g6));

p = [g1(g3); g1(g4); g2(g5); g2(g6)];

figure
spy(M(p,p))
