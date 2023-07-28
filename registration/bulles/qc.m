%set(0, 'DefaultFigureRenderer', 'opengl');
clear;
filepath="/mnt/storage/personal_data/dusiyuan/TZ14/step4/";
filepath2="/mnt/storage/personal_data/dusiyuan/TZ14/step4_symm/";
dirOutput=dir(fullfile(filepath,"*.csv"));
filenames={dirOutput.name};
p=ones(length(filenames),1);
for i=1:length(filenames)
    cd(filepath);
    a=csvread(filenames{i});
    cd(filepath2);
    b=csvread(filenames{i});
    temp=procrustes(a,b);
    p(i)=temp;
end