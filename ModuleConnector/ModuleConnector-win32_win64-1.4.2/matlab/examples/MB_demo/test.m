clear;
clc;
close all;
i = 0;
M=3;L=1;K=1;%K=1,M=2
pg=1;rx_num=2;
br_s=0;hr_s=0;
global flag1
flag1=1;
RawData=[];
hr=[];
br=[];
brstft=[];
hrstft=[];
time=[];
timestft=[];
startpoint=27;
endpoint=2392;
win=160;
Fs=20;
scale=449;
T=floor((endpoint-startpoint-win)/Fs+1);
load('C:\Users\zxy\Desktop\save\move.mat')
radar1=radar1(startpoint:endpoint,1:scale);
for i=1:T-1
    RawData=radar1((i-1)*Fs+1:(i-1)*Fs+win,:);
%     figure;
%     mesh(RawData);
    PureData=pca_filter_x4(RawData,rx_num,pg,M,L,K);
    tic
    [br_v,hr_v,t]=respiration_multi2(PureData);   %%% wavelet
%  	[br_v,hr_v,br_s,hr_s,t]=respiration_multi2_vncmd(PureData);   %%% VNCMD
    t1=toc-t
    RawData=[];
    hr=[hr;hr_v];
    br=[br;br_v];
    time=[time;t];
    
%     hrstft=[hrstft;hr_s];
%     brstft=[brstft;br_s];
%     timestft=[timestft;t1];
end 
% save('F:/radar/毕设/论文/radarmovevncmd300_10','hr','br','time')
% save('F:/radar/毕设/论文/radarmovestft','hrstft','brstft','timestft')
save('F:/radar/毕设/论文/radarmovewavelet','hr','br','time')