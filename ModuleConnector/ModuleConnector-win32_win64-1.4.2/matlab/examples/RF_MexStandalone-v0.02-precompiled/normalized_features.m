clear all
close all
clc

X=xlsread('F:\2017.11.8转移文件\xiu_features_final\queue\count_matlabcombine.xlsx');

X(:,3:35) = mapminmax(X(:,3:35),0,1);  %33
X(:,36:68) = mapminmax(X(:,36:68),0,1); %33
X(:,69:84) = mapminmax(X(:,69:84),0,1); %16
X(:,85:100) = mapminmax(X(:,85:100),0,1); %16
X(:,101:111) = mapminmax(X(:,101:111),0,1); %11
X(:,112:122) = mapminmax(X(:,112:122),0,1); %11
X(:,123:130) = mapminmax(X(:,123:130),0,1); %8
X(:,131:138) = mapminmax(X(:,131:138),0,1); %8
X(:,139:144) = mapminmax(X(:,139:144),0,1); %6
X(:,145:150) = mapminmax(X(:,145:150),0,1); %6
X(:,151:155) = mapminmax(X(:,151:155),0,1); %5
X(:,156:160) = mapminmax(X(:,156:160),0,1); %5
X(:,161:164) = mapminmax(X(:,161:164),0,1); %4
X(:,165:168) = mapminmax(X(:,165:168),0,1); %4

% xlswrite(['F:\2017.11.8转移文件\xiu_features_final\open lobby\count_matlabcombinenor1.xlsx'], X(1:40000,:));