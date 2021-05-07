function [people, PureData, mph]=newradar_signalprocessing(RawData)
M=0;L=0;K=1;
pg=1;rx_num=2;
PureData = pca_filter_x4(RawData,rx_num,pg,M,L,K);


NL=20;
NR=20;
%DirtyData=PowerData;
%[peaks,locs]=max(PureData(30,:));
mph1=100;
mph2=100;
mph3=100;
Iteration=10;
mpd=30;
%Adap=zeros(Batches,3);
%Adap=zeros(Batches,3,);
%figure;hold on;xlabel('thresholds');ylabel('row number');zlabel('peaks location');
spot1=cell(1,50);spot2=cell(1,50);spot3=cell(1,50);
for j=6:Batches
    [peaks,locs]=max(PureData(j,:));
       mph1=0.0009;
       mph2=0.001;
       mph3=0.0011;
    x=ones(1,Batches)*j;
    %[pks1,locs1]=findpeaks(PureData(j,:),'minpeakheight',mph1,'minpeakdistance',mpd); 
    DirtyData1=PureData(j,:);
    TOA1=[];
    k1=0;
    n1=0;
    for i=1:Iteration
        [val,loc]=max(DirtyData1);
        if loc>NL && loc<(size(PureData,2)-NR)
            if val>mph1
            if val>max(PureData(j,loc-NL:loc-1)) && val>max(PureData(j,loc+1:loc+NR))
                k1=k1+1;
                TOA1=[TOA1,loc];
            end
            DirtyData1(loc-NL:loc+NR)=0;
            i=i+1;
            end
        end
    end      
    %TOA1
    x=ones(1,length(TOA1))*j;
    y1=ones(1,length(TOA1))*mph1;
    z1=zeros(1,length(TOA1));
    for ii=1:length(TOA1)
        z1(ii)=TOA1(ii);
    end
    spot1(j)={TOA1};
    %plot3(y1,x,z1,'r.');
    %[pks2,locs2]=findpeaks(PureData(j,:),'minpeakheight',mph2,'minpeakdistance',mpd);
    DirtyData2=PureData(j,:);
    TOA2=[];
    k2=0;
    n2=0;
    for i=1:Iteration
        [val,loc]=max(DirtyData2);
        if loc>NL && loc<(size(PureData,2)-NR)
            if val>mph2
            if val>max(PureData(j,loc-NL:loc-1)) && val>max(PureData(j,loc+1:loc+NR))
                k2=k2+1;
                TOA2=[TOA2,loc];
            end
            DirtyData2(loc-NL:loc+NR)=0;
            i=i+1;
            end
        end
    end        
    x=ones(1,length(TOA2))*j;
    y2=ones(1,length(TOA2))*mph2;
    z2=zeros(1,length(TOA2));
    for ii=1:length(TOA2)
        z2(ii)=TOA2(ii);
    end
    spot2(j)={TOA2};
%     %plot3(y2,x,z2,'b.');
%     [pks3,locs3]=findpeaks(PureData(j,:),'minpeakheight',mph3,'minpeakdistance',mpd);
    DirtyData3=PureData(j,:);
    TOA3=[];
    k3=0;
    n3=0;
    for i=1:Iteration
        [val,loc]=max(DirtyData1);
        if loc>NL && loc<(size(PureData,2)-NR)
            if val>mph3
            if val>max(PureData(j,loc-NL:loc-1)) && val>max(PureData(j,loc+1:loc+NR))
                k3=k3+1;
                TOA3=[TOA3,loc];
            end
            DirtyData3(loc-NL:loc+NR)=0;
            i=i+1;
            end
        end
    end      
    x=ones(1,length(TOA3))*j;
    y3=ones(1,length(TOA3))*mph3;
    z3=zeros(1,length(TOA3));
    for ii=1:length(TOA3)
        z3(ii)=TOA3(ii);
    end
    spot3(j)={TOA3};
    %plot3(y3,x,z3,'g.');
end

sites1=[];num1=0;len1=[];
sites2=[];num2=0;len2=[];
sites3=[];num3=0;len3=[];
for ii=1:Batches
    temp1=cell2mat(spot1(ii));
    temp2=cell2mat(spot2(ii));
    temp3=cell2mat(spot3(ii));
    num1=length(temp1);
    num2=length(temp2);
    num3=length(temp3);
    len1=[len1,num1];
    len2=[len2,num2];
    len3=[len3,num3];
    for jj=1:num1
        sites1=[sites1;ii,temp1(jj)];
    end
    for jj=1:num2
        sites2=[sites2;ii,temp2(jj)];
    end
    for jj=1:num3
        sites3=[sites3;ii,temp3(jj)];
    end
end
num1=fix(median(len1))
num2=fix(median(len2))
num3=fix(median(len3))
var1=zeros(1,num1);
var2=zeros(1,num2);
var3=zeros(1,num3);
% 
if num1~=0
    [Idx1, C1, sumD1, D1] = kmeans(sites1(:,2), num1);
    for ii=1:num1
    var1(ii)=std(sites1(Idx1==ii,2));
    end
end
if num2~=0
    [Idx2, C2, sumD2, D2] = kmeans(sites2(:,2), num2);
    for ii=1:num2
    var2(ii)=std(sites2(Idx2==ii,2));
    end
end
if num3~=0
    [Idx3, C3, sumD3, D3] = kmeans(sites3(:,2), num3);
    for ii=1:num3
    var3(ii)=std(sites3(Idx3==ii,2));
    end
end
% %% Idx: 每个点所属的聚类标号
% %% C: 每类的质心
% %% numD: 1*K的和向量，存储的是类间所有点与该类质心点距离之和
% %% D: N*K的矩阵，存储的是每个点与所有质心的距离
% 
% 
% 
mean1=mean(var1);
mean2=mean(var2);
mean3=mean(var3);
min=0;
if mean1~=0
    min=mean1;
    if min>mean2&&mean2~=0
       min=mean2;
    end
    if min>mean3&&mean3~=0
        min=mean3;
    end
end
if num1==0&&num2==0&&num3==0
    mph=mph1;
    people=0;
end
    
%min
if min==mean1
    people=num1;
    mph=mph1;
elseif min==mean2
    people=num2;
    mph=mph2;
elseif min==mean3
    people=num3;
    mph=mph3;
end

