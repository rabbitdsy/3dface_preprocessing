addpath(genpath('C:\Users\user\Documents\Github\meshmonk\')) % change this to the correct path on your computer
rawpath="D:\3Dface\qingdao2\test\";
%rawpath="D:\3Dface\qingdao2\test\raw\";
objs = dir(strcat(rawpath,'*.obj'));
exportpath='D:\3Dface\qingdao2\test2\';
objsfinish = dir(strcat(exportpath,'*.obj'));
%exportpath="D:\3Dface\qingdao2\test\crop\";

parfor j=1:length(objs)
    cd(rawpath);
    name=objs(j).name;
    name=name(1:length(name)-4);
    Target = shape3D;
    Target.importWavefront(name, './');
    parsave2(Target,name,exportpath)
end

function parsave2(Target,name,path)
    save([path,name,'.mat'],'Target')
end