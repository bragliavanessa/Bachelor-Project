function [M,A,authors] = removeDuplicates(i,M,A, authors)
    m = size(i,2);
    to_delete = [];
    for p=1:m
        x=i(p);
        l = size(x{1},2);
        for k=2:l
            M(x{1}(1),:) = M(x{1}(1),:)+M(x{1}(k),:);
            to_delete = [to_delete x{1}(k)];
        end
        n = size(M,1);
        for j=1:n
            if M(x{1}(1),j)>1
                M(x{1}(1),j) = 1;
            end
        end
    end
    m = size(to_delete, 2);
    to_delete = sort(to_delete,'descend');
    to_delete
    m
    for p=1:m
        M(to_delete(p),:) = [];
        M(:,to_delete(p)) = [];
        A(to_delete(p)) = [];
        authors(to_delete(p)) = [];
    end
end