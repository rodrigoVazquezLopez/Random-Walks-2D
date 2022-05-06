obsFile = fopen("..\..\data\Experiment\obstacles_03May2022_12.40.txt","r");
obs = fscanf(obsFile, "(%f, %f), %f,\n", [3,inf]);
obs = obs';
obs(:,1) = obs(:,1)/100;
obs(:,2) = obs(:,2)/100;

figure;
hold on;
s = scatter(obs(:,1),obs(:,2),200,'filled');
xlim([-2.0,2.0]);
ylim([-2.0,2.0]);
grid on;
xticks(-2.05:0.1:2.05);
yticks(-2.05:0.1:2.05);
s.AlphaData = obs(:,3);
s.MarkerFaceAlpha = 'flat';

rndwlk = readmatrix("..\..\data\Experiment\randomWalk_03May2022_12.46.txt");
rndwlk = rndwlk/100;

plot(rndwlk(:,1),rndwlk(:,2), '-s','LineWidth',2, 'MarkerSize',10)

solution = readmatrix("..\..\data\Experiment\result_03May2022_12.46.txt");
solution = solution/100;

plot(solution(:,1),solution(:,2), '-s','LineWidth',2, 'MarkerSize',10)

dron1 = readmatrix("..\..\data\Experiment\Dron1_Vuelo_03May2022_12.46_log.txt");

plot(dron1(:,2),dron1(:,3), '-','LineWidth',2);

dron2 = readmatrix("..\..\data\Experiment\Dron2_Vuelo_03May2022_12.46_log.txt");

plot(dron2(:,2),dron2(:,3), '-','LineWidth',2);




