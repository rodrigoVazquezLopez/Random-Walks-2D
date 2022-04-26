list = dir("..\..\data\V2\22-Feb-22");
numFiles = (size(list, 1) - 2) / 2;

n = 50;
X = zeros(n*numFiles, 1);
Y = zeros(n*numFiles, 1);

F = zeros(n*numFiles, 3);

for i = 1:numFiles
    fileName = strcat(list(i+2).folder, '\', list(i+2).name);
    mov2D = readmatrix(fileName);
    X((n*(i-1)+1):i*n) = mov2D(:,2);
    Y((n*(i-1)+1):i*n) = mov2D(:,3);
end

V = [X Y];
Vdim = size(V, 1);

%writematrix(V,'puntos.txt','Delimiter',',')

idx = 1;
for i = 1:Vdim
    cnt = 0;
    if V(i,:) ~= [inf inf]
        tmp = V(i,:);
        for j = 1:Vdim    
            if V(j,:) == tmp
                cnt = cnt + 1;
                V(j,:) = [inf inf];
            end
        end
        F(idx, 1:2) = tmp;
        F(idx, 3) = cnt;
        idx = idx + 1;
    end
end

R = zeros(idx-1, 3);
R = F(1:idx-1, :);
alpha = zeros(idx-1,1);

maxVal = max(F(:,3));

for i = 1:idx-1
    R(i,3) = ((R(i,3) * 1) / maxVal);
end

writematrix(R,'puntos.txt','Delimiter',',');

s = scatter(R(:,1),R(:,2),200,'filled');
xlim([-2.0,2.0]);
ylim([-2.0,2.0]);
grid on;
xticks(-2.05:0.1:2.05);
yticks(-2.05:0.1:2.05);
s.AlphaData = R(:,3);
s.MarkerFaceAlpha = 'flat';



%plot(X,Y, '.', 'LineStyle','none','MarkerSize',15, 'MarkerEdgeColor','b','MarkerFaceColor',[0.5,0.5,0.5]);
%mov2D = readmatrix("..\..\data\V2\22-Feb-22\MovesTwoDim_22Feb2022_12.30_log.txt");
%plot(mov2D(:,2),mov2D(:,3), '.', 'LineStyle','none','MarkerSize',15, 'MarkerEdgeColor','b','MarkerFaceColor',[0.5,0.5,0.5]);
%xlim([-2.0,2.0]);
%ylim([-2.0,2.0]);

%grid on;

hold on
 
% plot([-0.4 1.3], [0.2, 0.4], '.', 'LineStyle','none','MarkerSize',15, 'MarkerEdgeColor','r','MarkerFaceColor',[0.5,0.5,0.5])
solution = readmatrix("..\..\solution.txt");
plot(solution(:,1)/100,solution(:,2)/100, '-s','LineWidth',2, 'MarkerSize',10)



