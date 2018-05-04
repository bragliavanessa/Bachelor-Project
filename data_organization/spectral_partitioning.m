function [g1,g2] = spectral_partitioning(M)
groups = [];
B = triu(M,1) ;
B = B + B';
deg = sum(B);
L = diag(deg)-B;

[V, ~] =eig(L); 
[~, p] =sort(V(:,2));
% spy(M(p,p))
% index1 = p(1:221); 
% index2 = p(221:end);
s = fix(size(p,1)/2);
g1 = p(1:s);
g2 = p(s:end);

% size(index1)
% size(index2)
% 
% group1=[];
% group2=[];
% 
% A = A(1,:);
% for i=1:size(index1,1)
%     group1 = [group1 A(index1(i))];
% end
% 
% for i=1:size(index2,1)
%     group2 = [group2 A(index2(i))];
% end
% 
% size(group1)
% size(group2)
% group1{1}
% group2{1}
% T = table(index1, group1', index2, group2');
% T.Properties.VariableNames{'Var2'} = 'Group1';
% T.Properties.VariableNames{'Var4'} = 'Group2';
end