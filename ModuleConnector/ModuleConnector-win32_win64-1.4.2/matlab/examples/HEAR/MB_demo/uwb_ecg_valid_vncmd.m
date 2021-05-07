 close all;clc;clear all;

DataPath='C:\Users\ayaya123\Desktop\ecg\ekg\';
uwbpath='C:\Users\ayaya123\Desktop\ecg\uwb\';
fileFolder=fullfile(DataPath);
dirOutput=dir(fullfile(fileFolder,'*.txt'));
fileNames={dirOutput.name}';
fileFolder_u=fullfile(uwbpath);
dirOutput_u=dir(fullfile(fileFolder_u,'*.mat'));
fileNames_u={dirOutput_u.name}';
PP=size(fileNames_u,1);

A=[]; QQ=25;BL=80;
temp=zeros(17,1);  
d2s=zeros(QQ,2000);fqc=zeros(4,QQ);

s=[DataPath,fileNames{1}];
fid=fopen(s,'r+','n','utf-8');
EKG=[];ecg_time=[];
 tline=fgetl(fid);
while ~feof(fid) 
      tline=fgetl(fid);
      %%读取debug下txt
      if length(tline)>21
         EKG=[EKG,str2num(tline(20:end))];
         s=[tline(1:4),tline(6:7),tline(9:10),tline(12:13),tline(15:16),tline(18:19)];
         ecg_time=[ecg_time;str2num(s)];
      end
end
fclose(fid);
% figure;plot(EKG)
% [RR,addr]=qrs3(EKG);

for ii=1:1
for jj=1:10
% u=load('F:\ProData\zll\static\1\radar\2016-07-15-20-50-13.txt');
u=load([uwbpath,fileNames_u{ii}]);
switch(ii)
    case 1, uwb_time=u.radar1(:,751); 
            RawData=u.radar1(:,1:750);
    case 2, uwb_time=u.radar2(:,751); 
            RawData=u.radar2(:,1:750);
    case 3, uwb_time=u.radar3(:,751); 
            RawData=u.radar3(:,1:750);
end
ecg_time=ecg_time-fix(ecg_time/(10^6))*10^6;

he=find(ecg_time-ecg_time(1)>0);
hu=find(uwb_time-uwb_time(1)>0);
head=max(ecg_time(he(1)),uwb_time(hu(1)));
tu=0;te=0;
te=find(ecg_time-ecg_time(end)<0);
tu=find(uwb_time-uwb_time(end)<0);
tail=min(ecg_time(te(end)),uwb_time(tu(end)));
bgn=find(ecg_time==head);
term=find(ecg_time==tail);
% [RR,addr]=qrs3(EKG(bgn(1):term(end)));%%s=EKG(bgn(1):term(end)); %% plot the heartbeat & ECG
len=fix((term(end)-bgn(1)+1)/QQ);
ekg_seg=EKG(bgn(1)+(jj-1)*len:bgn(1)+jj*len);
[RR,addr]=qrs3(EKG(bgn(1)+(jj-1)*len:bgn(1)+jj*len));
bgn=find(uwb_time==head);
term=find(uwb_time==tail);

M=0;L=0;K=1;
pg=1;rx_num=2;
br_s=0;hr_s=0;
PureData=pca_filter_x4(RawData(bgn(1):term(end),:),rx_num,pg,M,L,K);
c=size(PureData);
btm1=min(jj*BL,c(1));
bgn1=btm1-BL;
PicData=PureData(bgn1+1:btm1,:);
 RR=RR(find(RR>0))/512;
 hr_m=(length(RR)+1)/(sum(RR)/60); %% ECG心率

% [br_s,hr_s]=respiration_multi2(PicData(21:BL,101:750));  %% hr_s雷达心率，br_s雷达呼吸率
% temp=[hr_m;hr_s;br_s];
[br_v,hr_v]=respiration_multi2_vncmd(PicData(21:BL,101:750));
temp=[hr_m;hr_s;br_s];
% [br_v,hr_v,br_s,hr_s]=respiration_multi2_vncmd(PicData(21:BL,101:750)); 
% temp=[hr_m;br_v;hr_v;br_s;hr_s];

A=[A,temp];
end
end
A_mean=mean(A,2); 