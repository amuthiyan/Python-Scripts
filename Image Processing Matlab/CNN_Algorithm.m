%Importing the Digit dataset
digitDatasetPath = fullfile(matlabroot,'toolbox','nnet','nndemos','nndatasets','DigitDataset');
images = imageDatastore(digitDatasetPath,'IncludeSubfolders',true,'LabelSource','foldernames');
labels = images.Labels;

%Specify training dataset size and create training set
numTrainFiles = 50;
[trainset,testset] = splitEachLabel(images,numTrainFiles,'randomize');

%Implement the CNN algorithm from the paper:
layers = [
    imageInputLayer([28 28 1])
    
    convolution2dLayer(3,16,'Padding','same')
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,16,'Padding','same')
    
    maxPooling2dLayer(2,'Stride',2)
    
    fullyConnectedLayer(10)
    softmaxLayer
    classificationLayer];

options = trainingOptions('sgdm', ...
    'InitialLearnRate',0.01, ...
    'MaxEpochs',4, ...
    'Shuffle','every-epoch', ...
    'ValidationData',testset, ...
    'ValidationFrequency',30, ...
    'Verbose',false);

net = trainNetwork(trainset,layers,options);

pred_vec = classify(net,testset);
test_labels = testset.Labels;

accuracy = sum(pred_vec == test_labels)/numel(test_labels)

