c = A(1,:);
n = size(c,2);
for i=1:n
   for j=i+1:n
       if strcmp(A{i},A{j})
           i
           j
           A{i}
           A{j}
       end
   end
end