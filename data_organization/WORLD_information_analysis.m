%% Matrix visualization
figure
spy(MW)
title('authors adjacency matrix')

%% PageRank
% Call the function with swiss authors' information
TP = pagerank(authors_world,MW,0.85);
% Display the first 15 auhtors of the ranking
TP(1:10,:)

TPU = pagerank(univ_world,UW,0.85);
TPU(1:10,:)

%% Degree Centrality
% Rank authors only considering only number of collaboration and not
% quality
TD = degree_centrality(AW,MW);
TD(1:10,:)

%% The Reverse Cuthill McKee Ordering
r = symrcm(MW);
figure
subplot(1,2,1)
spy(MW);
title('Default connectivity matrix')
subplot(1,2,2)
spy(MW(r,r))
title('Ordered connectivity matrix')

% 1210
[lower,upper] = bandwidth(MW(r,r));

% Matrix sparsity = 2.4312e-04
sparsity = nnz(MW)/numel(MW);
