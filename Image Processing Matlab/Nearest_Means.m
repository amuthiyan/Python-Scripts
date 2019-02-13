train_file = fopen('data_training.txt');
formatSpec = '%d %d %d %d';
size_train = [4 Inf];

train_data = fscanf(train_file,formatSpec,size_train);
train_data = train_data';


classes = unique(train_data(1:8));

mean_0 = zeros(1,3);
mean_1 = zeros(1,3);

num0s = 0;
num1s = 0;

train_class = train_data(:,1);

train_data = train_data(:,2:4);

[num_rows,num_cols] = size(train_data);

%Testing
for row = 1:num_rows
    if train_class(row)==0
        num0s = num0s+1;
        for col = 1:num_cols
            %disp(train_data(row,col));
            mean_0(col) = mean_0(col) + train_data(row,col);
        end
    end
    if train_class(row)==1
        num1s = num1s+1;
        for col = 1:num_cols
            %disp(train_data(row,col));
            mean_1(col) = mean_1(col) + train_data(row,col);
            
        end
    end
end

mean_0 = mean_0/num0s;
mean_1 = mean_1/num1s;

%Testing
test_file = fopen('data_testing.txt');
formatSpec = '%d %d %d';
size_test = [3 Inf];

test_data = fscanf(test_file,formatSpec,size_test);
test_data = test_data';

[num_rows,num_cols] = size(test_data);

for row = 1:num_rows
    d0 = 0;
    d1 = 0;
    xm0 = 0;
    mm0 = 0;
    xm1 = 0;
    mm1 = 0;
    for col = 1:num_cols
        dp0 = mean_0(col)*test_data(row,col);
        dp1 = mean_1(col)*test_data(row,col);
        mtm0 = mean_0(col)*mean_0(col);
        mtm1 = mean_1(col)*mean_1(col);
        
        xm0 = xm0+dp0;
        xm1 = xm1+dp1;
        mm0 = mm0+mtm0;
        mm1 = mm1+mtm1;
    end
    mm0 = 0.5*mm0;
    mm1 = 0.5*mm1;
    
    d0 = xm0 - mm0;
    d1 = xm1 - mm1;
    
    disp('label:');
    if d0>d1
        disp(0);
    end
    if d1>d0
        disp(1);
    end
end

disp('Class 0');
disp(mean_0);
disp('Class 1');
disp(mean_1);
