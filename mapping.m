filename='0405796910.obj';
%% prepare for work 

% Add MeshMonk's toolbox to the working path and setup current folder
addpath(genpath('C:\Users\user\Documents\Github\meshmonk\')) % Set to location of meshmonk
%addpath('/data/dermatogenomics4/build/meshmonk/')   % Set to location of demo material
filepath = '../step1/';
savepath='../step3_mapping/';
demoFace = shape3D;
importWavefront(demoFace,filename,filepath,[]);
load 'Template.mat';
% Create an instance of the Shape Mapper class (obj)
obj = ShapeMapper;
obj.FloatingShape = clone(Template);      % Assign the Template to floating shape
obj.TargetShape = clone(demoFace);        % Assign the face to map to target shape

%% Rigid Registration
%obj.Display = true;                       % If false does not displays mapping process. When true, two windows appear:
										  % One shows the alignment of the template (white mesh) onto the target. The other shows how the
										  % template is being transformed during the registration, with yellow parts of the mesh
										  % classified as inliers and blue parts of the mesh classified as outliers.

% Predefined rigid mapping parameters, can be adjusted as desired 
obj.NumIterations = 10;                   % Number of iterations for the non-rigid registration
obj.InlierKappa = 3;                      % Threshold to consider a point as an outlier (+/- k times the standard deviation)
obj.TransformationType = 'rigid';         
obj.UseScaling = true;                    
obj.CorrespondencesNumNeighbours = 3;     % Number of k-nearest neighbors 
obj.CorrespondencesFlagThreshold = 0.9;
obj.CorrespondencesSymmetric = true;      % If false push forces are calculated (typical one-to-one correspondences). 
										  % When true: Pull-and-push forces are calculated 
obj.CorrespondencesEqualizePushPull = false;
obj.InlierUseOrientation = true;
obj.FlagFloatingBoundary = true;
obj.FlagTargetBoundary = true;
obj.FlagTargetBadlySizedTriangles = true; % Pruning large sized triangles 
obj.TriangleSizeZscore = 6;               % A large triangle is considered to fall x times the standard deviation from the mean
obj.UpSampleTarget = false;
% Mapping
tic;map(obj);time = toc;
fprintf ( 1, '  The Rigid Registration took %f seconds to run.\n', time );

%% Non-Rigid Registration

%obj.Display = true;                       % Same as above
% Predefined rigid mapping parameters, can be adjusted as desired 
nr = 10;                                 % Number of iterations for the non-rigid registration
obj.NumIterations = nr;                   % Number of iterations for the non-rigid registration
obj.TransformNumNeighbors = 80;           % Number of neighbors regularization
obj.CorrespondencesNumNeighbours = 3;     % Number of k-nearest neighbors
obj.CorrespondencesSymmetric = true;      % If false push forces are calculated (typical one-to-one correspondences). 
										  % When true: Pull-and-push forces are calculated 
obj.CorrespondencesFlagThreshold = 0.9;
obj.CorrespondencesUseOrientation = true;
obj.CorrespondencesEqualizePushPull =false;
obj.InlierKappa = 12;                     % Threshold to consider a point as an outlier (+/- k times the standard deviation)
obj.InlierUseOrientation = true;
obj.FlagFloatingBoundary = true;
obj.FlagTargetBoundary = true;
obj.FlagTargetBadlySizedTriangles = true; % Pruning large sized triangles 
obj.TriangleSizeZscore = 6;               % A large triangle is considered to fall x times the standard deviation from the mean
obj.UpSampleTarget = false;
obj.UseScaling = 1;
obj.TransformationType = 'nonrigid';
obj.TransformSigma = 3;
obj.TransformNumViscousIterationsStart = nr;
obj.TransformNumViscousIterationsEnd = 1;
obj.TransformNumElasticIterationsStart = nr;
obj.TransformNumElasticIterationsEnd = 1;
% Mapping
tic;map(obj);time = toc;
fprintf ( 1, '  The Non-Rigid Registration took %f seconds to run.\n', time );

%% Visualize Mapping result
%vref = viewer3D;                         % Create an instace of the viewer
%obj.TargetShape.ViewMode = 'points';     % Display as a point cloud
%obj.FloatingShape.ViewMode = 'points';
%obj.TargetShape.VertexSize = 10;         % Setup the size of the points
%obj.FloatingShape.VertexSize = 12;
%viewer(obj.FloatingShape,vref);          % Display the  Shape in the viewer
%viewer(obj.TargetShape,vref);


%% savefile
cd(savepath);
filesave = obj.FloatingShape;
name=[filename(1:length(filename)-3),'csv'];
%save(name,'filesave');
csvwrite(name,filesave.Vertices)