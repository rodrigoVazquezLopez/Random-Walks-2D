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
%     R(i,3) = ((R(i,3) * 1) / maxVal);
    R(i,3) = R(i,3) / j
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

figure
grid on;

[X,Y] = meshgrid(R(:,1),R(:,2));
Z = (X + Y)*0 + 1;
[Zf,Zc] = size(Z);
Z(112, 112) = 0.5; %
Z(112, 113) = 0.5; %
Z(112, 111) = 0.5; %
Z(113, 112) = 0.5; %
Z(113, 113) = 0.5; %
Z(113, 111) = 0.5; %
Z(111, 112) = 0.5; %
Z(111, 113) = 0.5; %
Z(111, 111) = 0.5; %
mesh(X,Y,Z)
%plot3(R(:,1),R(:,2),R(:,3),"-s",LineStyle="none",MarkerFaceColor=[0,0,0.7])
%bar3(R)

Z = zeros(31,25);
X = zeros(31,25);
Y = zeros(31,25);
[X,Y] = meshgrid( -1.0:0.1:1.4, -1.2:0.1:1.8);

%resultados = 0;
c= 0;
c2=0;
for i = -1.2:0.1:1.8
    c = c+1;
    c2 = 0;
    for j= -1.0:0.1:1.4
        c2 = c2 + 1;
        for k=1:223

            %X(c,) = R(k,1);
            %Y(c,c2) = R(k,2)
            %if(i==R(k,1) && j==R(k,2))
            if(i==X(c,c2) )
                Z(c,c2) = R(k,3);
                %Z(:,c2) = R(k,3)
               
                %resultados(k,1:3) = [i j Z(c, c2)];
            end
        end
    end
    
end



surf(X,Y,Z)

% Z = sin(X) + cos(Y);
% C = X.*Y;
% surf(X,Y,Z,C)
% colorbar

hold on
z = zeros(37,1);
plot3(solution(:,1)/100,solution(:,2)/100,z,'-s','LineWidth',2, 'MarkerSize',10)


