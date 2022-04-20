list = dir("..\..\data\V2\22-Feb-22");
numFiles = (size(list, 1) - 2) / 2;

n = 50;
X = zeros(n*numFiles, 1);
Y = zeros(n*numFiles, 1);

F = zeros(n*numFiles, 3);

for i = 1:11
    fileName = strcat(list(i+2).folder, '\', list(i+2).name);
    mov2D = readmatrix(fileName);
    X((n*(i-1)+1):i*n) = mov2D(:,2);
    Y((n*(i-1)+1):i*n) = mov2D(:,3);
end

histogram2(X,Y,30)
figure
%histogram(X,30)
%figure
%histogram(Y,30)

V = [X Y]

writematrix(V,'puntos.txt','Delimiter',',')

idx = 1
for i = 1:550
    cnt = 0;
    if V(i,:) ~= [inf inf]
        tmp = V(i,:);
        for j = 1:550    
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

R = zeros(idx-1, 3)
R = F(1:idx-1, :)

ref = max(F(:,3))




solution = readmatrix("..\..\solution.txt");
plot(X,Y, '.', 'LineStyle','none','MarkerSize',15, 'MarkerEdgeColor','b','MarkerFaceColor',[0.5,0.5,0.5]);
%mov2D = readmatrix("..\..\data\V2\22-Feb-22\MovesTwoDim_22Feb2022_12.30_log.txt");
%plot(mov2D(:,2),mov2D(:,3), '.', 'LineStyle','none','MarkerSize',15, 'MarkerEdgeColor','b','MarkerFaceColor',[0.5,0.5,0.5]);
xlim([-2.0,2.0]);
ylim([-2.0,2.0]);
xticks(-2.05:0.1:2.05);
yticks(-2.05:0.1:2.05);
grid on;
% %plot3(Vuelo1(:,1),Vuelo1(:,2),Vuelo1(:,3))
hold on
% a = -1.0
% b = 0
% x_i = round((b-a)*rand()+a,1)
% 
% a = 0
% b = 1.55
% y_i = round((b-a)*rand()+a,1)
% y_f = round((b-a)*rand()+a,1)
% 
% a = 1.05
% b = 1.55
% x_f = round((b-a)*rand()+a,1)
% 
% %plot([x_i x_f],[y_i y_f])
% 
% plot([-0.4 1.3], [0.2, 0.4], '.', 'LineStyle','none','MarkerSize',15, 'MarkerEdgeColor','r','MarkerFaceColor',[0.5,0.5,0.5])
plot(solution(:,1)/100,solution(:,2)/100, '-s','LineWidth',2, 'MarkerSize',10)
% 
% %ezplot('x^2+y^2-0.075')

