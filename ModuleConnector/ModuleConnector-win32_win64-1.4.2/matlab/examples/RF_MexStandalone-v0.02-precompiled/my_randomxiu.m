% A simple tutorial file to interface with RF
% Options copied from http://cran.r-project.org/web/packages/randomForest/randomForest.pdf

%run plethora of tests
clear all
clc
close all

%compile everything
if strcmpi(computer,'PCWIN') |strcmpi(computer,'PCWIN64')
   compile_windows
else
   compile_linux
end

total_train_time=0;
total_test_time=0;

%load the twonorm dataset 
% load data/twonorm
 
%modify so that training data is NxD and labels are Nx1, where N=#of
%examples, D=# of features   输入的X是data， Y是label

% X = inputs';
% Y = outputs;
% X=xlsread('F:\2017.11.8转移文件\Geoscience and Remote Sensing Letters\features\realdata\different_tester\open_bandpassdata\count_matlab.xlsx');
% X=xlsread('E:\xiu_features_final\open lobby\count_matlabrealtime.xlsx');
% X=xlsread('F:\2017.11.8转移文件\Geoscience_papers\统计数据\20180112\3ed+ct\count_3edct.xlsx');
% X= bsxfun(@rdivide, bsxfun(@minus, X, mean(X)), var(X)
% X= struct2cell(load('F:\2017.11.8转移文件\Geoscience_papers\统计数据\20180117\count_ct.mat'));
% X1 = struct2cell(load('F:\2017.11.8转移文件\Geoscience_papers\统计数据\20180117\test_ct.mat'));

X1=xlsread('C:\Users\mac\Desktop\0918车内\count.xlsx');
% X2=xlsread('C:\Users\mac\Desktop\车内不同雷达\雷达5\count.xlsx');

% X={X0{1,1};X1{1,1};X2{1,1};X3{1,1};X4{1,1}};
% X(7601:15200)=load('F:\2017.11.8转移文件\Geoscience_papers\统计数据\20180110_lessfeature\count_1.mat');
% Y= [zeros(7600, 1); ones(7600, 1)*1; ones(7600, 1)*2; ones(7600, 1)*3; ones(7600, 1)*4];
% Y1 = [ones(1900, 1)*2; ones(1330, 1)*3; ones(2850, 1)*4];
% Y= [zeros(165, 1); ones(165, 1)*1; ones(165, 1)*2; ones(165, 1)*3; ones(165, 1)*4; ones(165, 1)*5; ones(165, 1)*6; ones(165, 1)*7; ones(165, 1)*8;ones(165, 1)*9; ones(165, 1)*10; ones(165, 1)*11];
Y1= [zeros(150, 1); ones(100, 1)*1; ones(100, 1)*2; ones(100, 1)*3; ones(91, 1)*4];
% Y2= [zeros(10, 1); ones(10, 1)*1; ones(10, 1)*2; ones(10, 1)*3];
% Y1 = [ones(1410, 1)*2; ones(987, 1)*3; ones(2115, 1)*4];
% 
% X_mat = X{1,1};
% X1_mat = X1{1,1};

[N1 D1] =size(X1);
% [N D] =size(X_mat);
% [N1 D1] =size(X1_mat);
% %randomly split into 250 examples for training and 50 for testing
% %300行数据中用250条做训练，50条做测试
randvector1 = randperm(N1);
% [N2 D2] =size(X2);
% randvector2 = randperm(N2);

% randvector1 = randperm(N1);
% X_trn = X_mat(randvector(1:26600),:);
% Y_trn = Y(randvector(1:26600));
% X_tst = X_mat(randvector(26601:end),:);
% Y_tst = Y(randvector(26601:end));

% X_trn = X_mat(randvector(1:19740),:);
% Y_trn = Y(randvector(1:19740));
% X_tst = X_mat(randvector(19741:end),:);
% Y_tst = Y(randvector(19741:end));
% 
% X_trn = X(randvector(1:100),:);
% Y_trn = Y(randvector(1:100));
% X_tst = X(randvector(101:end),:);
% Y_tst = Y(randvector(101:end));

% X_trn = X1(randvector1(1:450),:);
% Y_trn = Y1(randvector1(1:450),:);
% X_tst = X1(randvector1(451:end),:);
% Y_tst = Y1(randvector1(451:end),:);

% % 
X_trn = X1(randvector1(1:end),:);
Y_trn = Y1(randvector1(1:end),:);
% X_tst = X2(randvector2(1:end),:);
% Y_tst = Y2(randvector2(1:end),:);
%%
% X_trn = X_mat(randvector(1:end),:);
% Y_trn = Y(randvector(1:end));
% X_tst = X1_mat(randvector1(1:end),:);
% Y_tst = Y1(randvector1(1:end));

% X_trn = X_mat(1:end,2);
% Y_trn = Y(1:end);
% randvector1 = randperm(N1);
% X_trn = X_mat;
% Y_trn = Y;
% X_tst = X_mat(1:1000,2);
% Y_tst = Y(1:1000);

% X_trn = X_mat(randvector(1:109440),:);
% Y_trn = Y(randvector(109441:end));
% X_tst = X1_mat(randvector1(1:109440),:);
% Y_tst = Y1(randvector1(108441:end));

% X_trn = X_mat(:,3:6);
% Y_trn = Y;
% 
% X_tst = X1_mat(:,3:6);
% Y_tst = Y1;

% X1 = xlsread('F:\2017.11.8转移文件\Geoscience_papers\统计数据\20180112\3ed+ct\test_3edct.xlsx');
% Y1 = [ones(1410, 1)*2; ones(987, 1)*3; ones(2115, 1)*4];
% % Y1 = [ones(1900, 1)*2; ones(1330, 1)*3; ones(2850, 1)*4];
% [N1 D1] =size(X1);
% randvector1 = randperm(N1);
% % % % % X_trn = X;
% % % % % Y_trn = Y;
% % % % % 
% X_tst = X1(randvector1(1:end),:);
% Y_tst = Y1(randvector1(1:end));

% X_tst = X1{1,1};
% Y_tst = Y1;
% 
% % example 1:  simply use with the defaults
    model = classRF_train(X_trn,Y_trn,50);
    save('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\newxiu_incar2018920','model');
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 1: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
%     fprintf('\nexample 1: accuracy %f\n',   length(find(Y_hat==Y_tst))/length(Y_tst));
% example 2:  set to 100 trees
%     model = classRF_train(X_trn,Y_trn, 100);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 2: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
% 
% example 3:  set to 100 trees, mtry = 2
%     model = classRF_train(X_trn,Y_trn, 100,2);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 3: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
% 
% % example 4:  set to defaults trees and mtry by specifying values as 0
%     model = classRF_train(X_trn,Y_trn, 0, 0);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 4: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
% 
% % example 5: set sampling without replacement (default is with replacement)
%     extra_options.replace = 0 ;
%     model = classRF_train(X_trn,Y_trn, 100, 4, extra_options);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 5: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
% 
% % example 6: Using classwt (priors of classes)
%     clear extra_options;
%     extra_options.classwt = [1 1]; %for the [-1 +1] classses in twonorm
%     % if you sort the labels in training and arrange in ascending order then
%     % for twonorm you have -1 and +1 classes, with here assigning 1 to
%     % both classes
%     % As you have specified the classwt above, what happens that the priors are considered
%     % also is considered the freq of the labels in the data. If you are
%     % confused look into src/rfutils.cpp in normClassWt() function
% 
%     model = classRF_train(X_trn,Y_trn, 100, 4, extra_options);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 6: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
% 
% % example 7: modify to make class(es) more IMPORTANT than the others
%     %  extra_options.cutoff (Classification only) = A vector of length equal to
%     %                       number of classes. The 'winning' class for an observation is the one with the maximum ratio of proportion
%     %                       of votes to cutoff. Default is 1/k where k is the number of classes (i.e., majority
%     %                       vote wins).    clear extra_options;
%     extra_options.cutoff = [1/4 3/4]; %for the [-1 +1] classses in twonorm
%     % if you sort the labels in training and arrange in ascending order then
%     % for twonorm you have -1 and +1 classes, with here assigning 1/4 and
%     % 3/4 respectively
%     % thus the second class needs a lot less votes to win compared to the first class
%     
%     model = classRF_train(X_trn,Y_trn, 100, 4, extra_options);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 7: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
%     fprintf('   y_trn is almost 50/50 but y_hat now has %f/%f split\n',length(find(Y_hat~=-1))/length(Y_tst),length(find(Y_hat~=1))/length(Y_tst));
    

%  extra_options.strata = (not yet stable in code) variable that is used for stratified
%                       sampling. I don't yet know how this works.
% 
% % example 8: sampsize example
%     %  extra_options.sampsize =  Size(s) of sample to draw. For classification, 
%     %                   if sampsize is a vector of the length the number of strata, then sampling is stratified by strata, 
%     %                   and the elements of sampsize indicate the numbers to be drawn from the strata.
%     clear extra_options
%     extra_options.sampsize = size(X_trn,1)*2/3;
%     
%     model = classRF_train(X_trn,Y_trn, 100, 4, extra_options);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 8: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
%     
% % example 9: nodesize
%     %  extra_options.nodesize = Minimum size of terminal nodes. Setting this number larger causes smaller trees
%     %                   to be grown (and thus take less time). Note that the default values are different
%     %                   for classification (1) and regression (5).
%     clear extra_options
%     extra_options.nodesize = 2;
%     
%     model = classRF_train(X_trn,Y_trn, 100, 4, extra_options);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 9: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
%         
% % 
% % % % % example 10: calculating importance
%     clear extra_options
%     extra_options.importance = 1; %(0 = (Default) Don't, 1=calculate)
%    
%     model = classRF_train(X_trn,Y_trn, 5, 4, extra_options);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 10: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
% %     
% %     %model will have 3 variables for importance importanceSD and localImp
% %     %importance = a matrix with nclass + 2 (for classification) or two (for regression) columns.
% %     %           For classification, the first nclass columns are the class-specific measures
% %     %           computed as mean decrease in accuracy. The nclass + 1st column is the
% %     %           mean decrease in accuracy over all classes. The last column is the mean decrease
% %     %           in Gini index. For Regression, the first column is the mean decrease in
% %     %           accuracy and the second the mean decrease in MSE. If importance=FALSE,
% %     %           the last measure is still returned as a vector.
%     figure('Name','Importance Plots')
%     subplot(2,1,1);
%     bar(model.importance(:,end-1));xlabel('feature');ylabel('magnitude');
%     title('Mean decrease in Accuracy');
%     
%     subplot(2,1,2);
%     bar(model.importance(:,end));xlabel('feature');ylabel('magnitude');
%     title('Mean decrease in Gini index');
    
%     
%     importanceSD = The ?standard errors? of the permutation-based importance measure. For classification,
%               a D by nclass + 1 matrix corresponding to the first nclass + 1
%               columns of the importance matrix. For regression, a length p vector.
%     model.importanceSD
% 
% % example 11: calculating local importance
%     %  extra_options.localImp = Should casewise importance measure be computed? (Setting this to TRUE will
%     %                   override importance.)
%     %localImp  = a D by N matrix containing the casewise importance measures, the [i,j] element
%     %           of which is the importance of i-th variable on the j-th case. NULL if
%     %          localImp=FALSE.
%     clear extra_options
%     extra_options.localImp = 1; %(0 = (Default) Don't, 1=calculate)
%    
%     model = classRF_train(X_trn,Y_trn, 100, 4, extra_options);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 11: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
% 
%     model.localImp
%     
% % example 12: calculating proximity
%     %  extra_options.proximity = Should proximity measure among the rows be calculated?
%     clear extra_options
%     extra_options.proximity = 1; %(0 = (Default) Don't, 1=calculate)
%    
%     model = classRF_train(X_trn,Y_trn, 100, 4, extra_options);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 12: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
% 
%     model.proximity
%     
% 
% % example 13: use only OOB for proximity
%     %  extra_options.oob_prox = Should proximity be calculated only on 'out-of-bag' data?
%     clear extra_options
%     extra_options.proximity = 1; %(0 = (Default) Don't, 1=calculate)
%     extra_options.oob_prox = 0; %(Default = 1 if proximity is enabled,  Don't 0)
%    
%     model = classRF_train(X_trn,Y_trn, 100, 4, extra_options);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 13: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
% 
% 
% % example 14: to see what is going on behind the scenes    
% %  extra_options.do_trace = If set to TRUE, give a more verbose output as randomForest is run. If set to
% %                   some integer, then running output is printed for every
% %                   do_trace trees.
%     clear extra_options
%     extra_options.do_trace = 1; %(Default = 0)
%    
%     model = classRF_train(X_trn,Y_trn, 100, 4, extra_options);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 14: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
% 
% % example 14: to see what is going on behind the scenes    
% %  extra_options.keep_inbag Should an n by ntree matrix be returned that keeps track of which samples are
% %                   'in-bag' in which trees (but not how many times, if sampling with replacement)
% %
%     clear extra_options
%     extra_options.keep_inbag = 1; %(Default = 0)
%    
%     model = classRF_train(X_trn,Y_trn, 100, 4, extra_options);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 15: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
%     
%     model.inbag
% 
% % example 16: getting the OOB rate. model will have errtr whose first
% % column is the OOB rate. and the second column is for the 1-st class and
% % so on
%     model = classRF_train(X_trn,Y_trn);
%     Y_hat = classRF_predict(X_tst,model);
%     fprintf('\nexample 16: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
%     
%     figure('Name','OOB error rate');
%     plot(model.errtr(:,1)); title('OOB error rate');  xlabel('iteration (# trees)'); ylabel('OOB error rate');
%     
% 
% % example 17: getting prediction per tree, votes etc for test set
%     model = classRF_train(X_trn,Y_trn);
%     
%     test_options.predict_all = 1;
%     [Y_hat, votes, prediction_pre_tree] = classRF_predict(X_tst,model,test_options);
%     fprintf('\nexample 17: error rate %f\n',   length(find(Y_hat~=Y_tst))/length(Y_tst));
    


