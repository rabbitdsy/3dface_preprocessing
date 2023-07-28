addpath(genpath('C:\Users\user\Documents\Github\meshmonk\')); % change this to the correct path on your computer
Target = shape3D;
Target.importWavefront('FINAL.obj', './');
Target.Material='Facial';
Target.ColorMode='Indexed'
fragile=clone(Target);
pudong=clone(Target);
fragile_point=importdata('ADNP_all_avg2.csv');
fragile_point=fragile_point;%.data;
pudong_point=importdata('all_avg.csv');
pudong_point=pudong_point;%.data;

fragile.Vertices=fragile_point;
%fragile.Vertices=fragile_point/fragile.CentroidSize;

pudong.Vertices=pudong_point;
%pudong.Vertices=pudong_point/pudong.CentroidSize;

nomral_displacement=sum((fragile.Vertices-pudong.Vertices).* pudong.VertexNormals,2);
%sig=nomral_displacement/abs(nomral_displacement);   %

%distance=sum((fragile.Vertices-pudong.Vertices).*(fragile.Vertices-pudong.Vertices),2);%
%nomral_displacement=sig*distance;%


display=clone(pudong);
display.VertexValue=nomral_displacement;
mx=max(abs(nomral_displacement));

%% 画图   带色彩的
v=display.Vertices;
theta = 0;    %调角度
% 构建旋转矩阵
Rx = [1,0,0;
    0,cos(theta), sin(theta);
     0,-sin(theta), cos(theta);];

Ry = [cos(theta), 0, sin(theta);
     0, 1, 0;
     -sin(theta), 0, cos(theta)];
 
Rz = [cos(theta), sin(theta), 0;
     -sin(theta), cos(theta), 0;
     0, 0 ,1;];
 
v=v*Ry;

colorMin = -mx;
colorMax = mx;
n=10000;
% 生成红到白再到蓝的连续颜色映射
WhiteToRed = [linspace(1, 1, n)', linspace(1, 0, n)', linspace(1, 0, n)'];
BlueToWhite = [linspace(0, 1, n)', linspace(0, 1, n)', linspace(1, 1, n)'];
customColormap = [BlueToWhite; WhiteToRed];

axes('DataAspectRatio', [1 1 1], 'Visible', 'on');
axis vis3d;
patch('vertices',v,'faces',display.Faces,'FaceVertexCData', display.VertexValue);
colormap(customColormap);
caxis([colorMin colorMax]);
shading flat;
lighting flat;
material dull;
camlight('headlight');
camproj('perspective');
axis equal;
colorbar;
ax = gca;
ax.Visible = 'off';



%% 画图 没色彩的
display=fragile; %%%%也可以是fragile/浦东
v=display.Vertices;
theta = pi/4;    %%调角度
% 构建旋转矩阵
Ry = [cos(theta), 0, sin(theta);
     0, 1, 0;
     -sin(theta), 0, cos(theta)];
 
Rx = [cos(theta), sin(theta), 0;
     -sin(theta), cos(theta), 0;
     0, 0 ,1;];
 
v=v*Rx;
axes('DataAspectRatio', [1 1 1], 'Visible', 'on');
axis vis3d;
patch('vertices',v,'faces',display.Faces,'FaceVertexCData', zeros(size(Target.Vertices,1),1));

customColormap  = [
    0.8, 0.8, 0.8;      % 黑色
    0.8,0.8,0.8% 蓝色
];
colormap(customColormap);
shading flat;
lighting flat;
material dull;
camlight('headlight');
camproj('perspective');
axis equal;
ax = gca;
ax.Visible = 'off';