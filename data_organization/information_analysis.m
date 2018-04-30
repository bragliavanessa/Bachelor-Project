%% PageRank
% Call the function with swiss authors' information
TP = pagerank(authors,M,0.85);
% Display the first 15 auhtors of the ranking
TP(1:15,:)

% T = T(1:15,:);
% figure
% TString = evalc('disp(T)');
% 
% % Use TeX Markup for bold formatting and underscores.
% TString = strrep(TString,'<strong>','\bf');
% TString = strrep(TString,'</strong>','\rm');
% TString = strrep(TString,'_','\_');
% 
% % Get a fixed-width font.
% FixedWidth = get(0,'FixedWidthFontName');
% 
% % Output the table using the annotation command.
% annotation(gcf,'Textbox','String',TString,'Interpreter','Tex',...
%     'FontName',FixedWidth,'Units','Normalized','Position',[0 0 1 1]);

%% Degree Centrality
% Rank authors only considering only number of collaboration and not
% quality
TD = degree_centrality(A,M);
TD(1:10,:)

%% Spectral graph Partitioning
TS = spectral_partitioning(M,A);
TS(1:10,:)