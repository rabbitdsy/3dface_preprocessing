addpath(genpath('C:\Users\user\Documents\Github\meshmonk\')) % change this to the correct path on your computer
parentpath='D:\3Dface\qingdao2\';  %path最后都记得有斜杠，以单引号包围
rawpath=[parentpath 'center_obj_mat' '\'];
allobjs=[parentpath 'allobjs.mat'];
%% 初次使用运行这里生成allobjs.mat
%objs = dir(strcat(rawpath,'*.mat'));
%for i=1:length(objs)
%    objs(i).finish = 0;
%    objs(i).delete = 0;
%end
%objs=flip(objs);
%save('D:\3Dface\qingdao2\allobjs.mat','objs')
%% 
exportpath=[parentpath 'crop_obj' '\'];
finishpath=[parentpath 'center_obj_mat_finish' '\'];
deletepath=[parentpath 'center_obj_mat_delete' '\'];

load(allobjs)
ind=find([objs.finish]==0);ind=ind(1);
for j=ind:length(objs)
    cd(rawpath);
    name=objs(j).name;    
    load(name);    

    global breakValue;
    breakValue = 0;
    global SideValue;
    SideValue = 0;
    global saveValue;
    saveValue = 1;
    % 创建三维坐标系
    while breakValue == 0
        if SideValue==0
            v = Target.Vertices;
            v(:,3) = v(:,3)+100;
        end
        
        if SideValue==1
            v = Target.Vertices;
            v(find(v(:,1)<0),3)=0;
            v(find(v(:,1)<0),2)=0;
            % 定义旋转角度（弧度）
            theta = pi/2;
            % 构建旋转矩阵
            R = [cos(theta), 0, sin(theta);
                 0, 1, 0;
                 -sin(theta), 0, cos(theta)];
             v=v*R;
        end
        
        if SideValue==-1
            v = Target.Vertices;
            v(find(v(:,1)>0),3)=0;
            v(find(v(:,1)>0),2)=0;
            % 定义旋转角度（弧度）
            theta = -pi/2;
            % 构建旋转矩阵
            R = [cos(theta), 0, sin(theta);
                 0, 1, 0;
                 -sin(theta), 0, cos(theta)];
             v=v*R;
        end
       %% Figure 参数
        figure;
        title(name(1:length(name)-4));
        figPosition = [1000, 100, 900,700 ]; % 示例宽度800像素，高度600像素
        set(gcf, 'Position', figPosition);
       %% 多个button
        %结束按钮
        btn = uicontrol('Style', 'pushbutton', 'String', '保存(按一下点两下空白)', ...
            'Position', [0 50 130 30], 'Callback', @buttonCallback);
        cancel = uicontrol('Style', 'pushbutton', 'String', '取消', ...
            'Position', [0 80 130 30], 'Callback', @buttonCallbackCancel);
        %正面按钮  
        btn2 = uicontrol('Style', 'pushbutton', 'String', '左侧', ...
            'Position', [0 110 130 30], 'Callback', @buttonCallbackLeft);
        
        btn3 = uicontrol('Style', 'pushbutton', 'String', '右侧', ...
            'Position', [0 140 130 30], 'Callback', @buttonCallbackRight);
        btn1 = uicontrol('Style', 'pushbutton', 'String', '正面', ...
            'Position', [0 170 130 30], 'Callback', @buttonCallbackFront);
        btnsave = uicontrol('Style', 'pushbutton', 'String', 'delete', ...
            'Position', [0 200 130 30], 'Callback', @buttonCallbackDelete);
        
        %% 画图参数
        axes('DataAspectRatio', [1 1 1], 'Visible', 'on');
        axis vis3d;
        cntr=mean(Target.Vertices,1);
        tval=zeros(size(Target.Vertices,1),1);
        for i=1:size(Target.Vertices,1)
            tval(i,1)=norm(Target.Vertices(i,:)-cntr);
        end
        % display object
        patch('vertices',v,'faces',Target.Faces,'FaceVertexCData', tval);
        shading flat;
        customColormap  = [
            0.8, 0.8, 0.8;      % 黑色
            0.8,0.8,0.8% 蓝色
        ];
        % 应用自定义 colormap
        colormap(customColormap);
        lighting flat;
        material dull;
        camlight('headlight');
        camproj('orthographic');
        axis equal;


        %% 启用交互式切割
        %h = imfreehand;
        h = drawfreehand;  
        %wait(h);
        position = h.Position;
        w = waitforbuttonpress();
        if w==1
            if SideValue==0
                in=inpolygon(Target.Vertices(:,1),Target.Vertices(:,2),position(:,1),position(:,2));
                Target.crop('VertexIndex',find(in==0));
            end
            
            if SideValue==1
                in=inpolygon(-Target.Vertices(:,3),Target.Vertices(:,2),position(:,1),position(:,2));
                index = intersect(find(Target.Vertices(:,1)>0),find(in==1));
                index2 = setdiff(1:length(Target.Vertices),index);
                Target.crop('VertexIndex',index2);
            end
                        if SideValue==-1
                in=inpolygon(Target.Vertices(:,3),Target.Vertices(:,2),position(:,1),position(:,2));
                index = intersect(find(Target.Vertices(:,1)<0),find(in==1));
                index2 = setdiff(1:length(Target.Vertices),index);
                Target.crop('VertexIndex',index2);
            end
        end
        close();

    end
    breakValue=0;
    if saveValue==1
        cd(exportpath);
        Target.exportWavefront([name(1:length(name)-4) '.obj'],'./');
        movefile([rawpath,objs(j).name], finishpath);
        objs(j).finish=1;
    end
    if saveValue==0
        %delete(name);
        movefile([rawpath,objs(j).name], deletepath);
        objs(j).delete=1;
        objs(j).finish=1;
    end
    save(allobjs,'objs')
    saveValue=1;
end


function buttonCallback(hObject, eventdata)
    global breakValue;
    breakValue = 1;
end

function buttonCallbackCancel(hObject, eventdata)
    global breakValue;
    breakValue = 0;
    global saveValue
    saveValue = 1;
end

function buttonCallbackFront(hObject, eventdata)
    global SideValue
    SideValue = 0;
end

function buttonCallbackLeft(hObject, eventdata)
    global SideValue
    SideValue = -1;
end

function buttonCallbackRight(hObject, eventdata)
    global SideValue
    SideValue = 1;
end

function buttonCallbackDelete(hObject, eventdata)
    global saveValue
    saveValue = 0;
end