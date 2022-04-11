list = dir("..\..\data\V2\22-Feb-22");

n = 50;
X = zeros(n*11, 1);
Y = zeros(n*11, 1);

for i = 1:11
    fileName = strcat(list(i+2).folder, '\', list(i+2).name);
    mov2D = readmatrix(fileName);
    X((50*(i-1)+1):i*n) = mov2D(:,2);
    Y((50*(i-1)+1):i*n) = mov2D(:,2);
end

histogram2(X,Y,500)
figure
%histogram(X,30)
%figure
%histogram(Y,30)

V = [X Y]

writematrix(V,'puntos.txt','Delimiter',',') 

solution = readmatrix("..\..\solution.txt");
mov2D = readmatrix("..\..\data\V2\22-Feb-22\MovesTwoDim_22Feb2022_12.30_log.txt");
plot(mov2D(:,2),mov2D(:,3), '.', 'LineStyle','none','MarkerSize',15, 'MarkerEdgeColor','b','MarkerFaceColor',[0.5,0.5,0.5]);
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
