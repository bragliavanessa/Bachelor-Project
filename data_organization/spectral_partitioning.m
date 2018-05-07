function [g1,g2] = spectral_partitioning(M)

B = M;
deg = sum(B);
L = diag(deg)-B;


[V, ~] =eig(L); 
[~, p] =sort(V(:,2));

s = fix(size(p,1)/2);
g1 = p(1:s);
g2 = p(s+1:end);


end