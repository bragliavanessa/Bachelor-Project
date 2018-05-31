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
TP(1:10,:)

TPU = pagerank(univ,U,0.85);
TPU(1:10,:)

%% Degree Centrality
% Rank authors only considering only number of collaboration and not
% quality
TD = degree_centrality(A,M);
TD(1:10,:)

%% The Reverse Cuthill McKee Ordering
r = symrcm(M);
figure
subplot(1,2,1)
spy(M);
title('Default connectivity matrix')
subplot(1,2,2)
spy(M(r,r))
title('Ordered connectivity matrix')


% p2 = amd(M);
% new2 = authors(p2,:);
% figure
% spy(M(p2,p2))

% 48
[lower,upper] = bandwidth(M(r,r));
L=M(r,r);

% Matrix sparsity = 0.0085
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

Mp = M(p,p);
m = size(Mp,1);
n = size (M,1);


N1 = zeros(n,n);
n1 = size(g1(g3),1);
ll = 1;
lu = n1;
N1(ll:lu,ll:lu) = Mp(ll:lu,ll:lu);
% N1(1:m,1:l) = Mp(1:m,1:l);

n2 = size(g1(g4),1);
lu = lu + n2;
ll = ll + n1;
N2 = zeros(n,n);
N2(ll:lu,ll:lu) = Mp(ll:lu,ll:lu);
% N(n1+1:m,n1+1:l) = Mp(n1+1:m,n1+1:n1+n2);

N3 = zeros(n,n);
n3 = size(g2(g5),1);
lu = lu + n3;
ll = ll + n2;
N3(ll:lu,ll:lu) = Mp(ll:lu,ll:lu);
% N3(n1+n2+1:n1+n2+n3,n1+n2+1:m) = Mp(n1+n2+1:n1+n2+n3,n1+n2+1:m);
% N3(n1+n2+1:m,n1+n2+1:n1+n2+n3) = Mp(n1+n2+1:m,n1+n2+1:n1+n2+n3);

N4 = zeros(n,n);
n4 = size(g2(g6),1);
lu = lu + n4;
ll = ll + n3;
N4(ll:lu,ll:lu) = Mp(ll:lu,ll:lu);
% N4(n1+n2+n3+1:n1+n2+n3+n4,n1+n2+n3+1:m) = Mp(n1+n2+n3+1:n1+n2+n3+n4,n1+n2+n3+1:m);
% N4(n1+n2+n3+1:m,n1+n2+n3+1:n1+n2+n3+n4) = Mp(n1+n2+n3+1:m,n1+n2+n3+1:n1+n2+n3+n4);


figure
spy(N1, 'm')
hold on
spy(N2, 'b')
hold on
spy(N3, 'r')
hold on
spy(N4, 'c')
nz = nnz(N1)+nnz(N2)+nnz(N3)+nnz(N4);
xlabel(sprintf('nz = %d',nz));
[~, b] = legend('group 1','group 2', 'group 3', 'group 4');
set(findobj(b,'-property','MarkerSize'),'MarkerSize',15)

