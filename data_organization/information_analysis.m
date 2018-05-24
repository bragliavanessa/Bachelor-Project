%% Matrix visualization
figure
spy(M)
title('authors adjacency matrix')

figure
spy(U)
title('universities adjacency matrix')

figure
imagesc(W)
colorbar
title('universities weighted adjacency matrix')

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

% Visualizzare di diversi colori
% hold on tra una e l'altra


p = [g1(g3); g1(g4); g2(g5); g2(g6)];

Mp = M(p,p);
m = size(Mp,1);

N1 = zeros(size (M,1),size (M,1));
n1 = size(g1(g3),1);
N1(1:n1,1:m) = Mp(1:n1,1:m);
N1(1:m,1:n1) = Mp(1:m,1:n1);


N2 = zeros(size (M,1),size (M,1));
n2 = size(g1(g4),1);
N2(n1+1:n1+n2,n1+1:m) = Mp(n1+1:n1+n2,n1+1:m);
N2(n1+1:m,n1+1:n1+n2) = Mp(n1+1:m,n1+1:n1+n2);

N3 = zeros(size (M,1),size (M,1));
n3 = size(g2(g5),1);
N3(n1+n2+1:n1+n2+n3,n1+n2+1:m) = Mp(n1+n2+1:n1+n2+n3,n1+n2+1:m);
N3(n1+n2+1:m,n1+n2+1:n1+n2+n3) = Mp(n1+n2+1:m,n1+n2+1:n1+n2+n3);

N4 = zeros(size (M,1),size (M,1));
n4 = size(g2(g6),1);
N4(n1+n2+n3+1:n1+n2+n3+n4,n1+n2+n3+1:m) = Mp(n1+n2+n3+1:n1+n2+n3+n4,n1+n2+n3+1:m);
N4(n1+n2+n3+1:m,n1+n2+n3+1:n1+n2+n3+n4) = Mp(n1+n2+n3+1:m,n1+n2+n3+1:n1+n2+n3+n4);


figure
spy(N1, 'r')
hold on
spy(N2, 'b')
hold on
spy(N3, 'g')
hold on
spy(N4, 'y')

figure 
spy(M(p,p))
