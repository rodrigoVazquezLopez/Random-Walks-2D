clear; clc; clf;
R=readmatrix('puntos.txt','Delimiter',',');
R2=round(R(:,1:2),1);

xi=round(-1.2:0.1:1.2,1);
yi=round(-1.2:0.1:1.8,1);
[X,Y] = meshgrid(xi,yi);
[f,c]=size(R);

for i=1:f
    xp = find(xi==R2(i,2));
    yp = find(yi==R2(i,1));  
    MZ(yp,xp)=R(i,3);
end

surf(X,Y,MZ,'FaceAlpha',0.8)
colorbar