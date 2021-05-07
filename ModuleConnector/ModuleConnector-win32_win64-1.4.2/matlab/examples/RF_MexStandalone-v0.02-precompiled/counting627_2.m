function [people] =counting627_2(RawData)
FrameStitchnum=size(RawData,2)/256;
SpeedOfLight=3*10^8;
Resolution=0.00386751476861213;
Fs=SpeedOfLight/(Resolution*2);
[bandfilter]=qfir(Fs);
%Receive Raw Data
fornum=200;
Batches=50;
% RawData=zeros(Batches,256*FrameStitchnum);
% BandpassData=zeros(Batches,256*FrameStitchnum);
% ClutterData=zeros(Batches,256*FrameStitchnum);
% PureData=zeros(Batches,256*FrameStitchnum);
pnum=256;
firnum=100;
alpha=0.6;
people=0;
Iteration=10;

% M=[1:pnum*FrameStitchnum];
% wt=exp(-(2*(M/256).^2));
% for i=1:fornum
for raw=1:1:Batches
    for framenum=1:FrameStitchnum
        blockdata=RawData(raw,(framenum-1)*pnum+1:framenum*pnum);
        blockmean=mean(blockdata);
        DCmean=repmat(blockmean,1,pnum);
        RawData(raw,(framenum-1)*pnum+1:framenum*pnum)=blockdata-DCmean;      
    end
        convres=conv(RawData(raw,:),bandfilter);
        BandpassData(raw,:)=convres(1,firnum/2+1:firnum/2+256*FrameStitchnum);
end
% %%%%%%%%%%%%%%%%%%%Kalman Filter__Calculate noise%%%%%%%%%%%%%%%%%%%%%%%
sigma=1;
C = fdct_wrapping(BandpassData,1,2);
E = cell(size(C));
 for s=1:length(C)
   E{s} = cell(size(C{s}));
   for w=1:length(C{s})
     A = C{s}{w};
     E{s}{w} = median(abs(A(:) - median(A(:))))/-6.3255; 
   end
 end
Ct=C;
 %对每个子带的变换系数做硬阈值处理
for s = 2:length(C)
  thresh = 3*sigma + sigma*(s == length(C));
  
%在阈值的选取上,是保留较大的系数,舍弃较小的系数, 因为根据Curvelet变换理论, 较大的Curvelet系数对应于较强的边缘,反之为噪声
  for w = 1:length(C{s})
    Ct{s}{w} = C{s}{w}.* (abs(C{s}{w}) < thresh*E{s}{w});
  end
end
%   
noise=ifdct_wrapping(Ct,1);
% % %%%%%%%%%%%%%%%%%%%Kalman Filter__Calculate noise%%%%%%%%%%%%%%%%%%%%%%%
Qk = 0.02;  
ClutterData2=zeros(Batches,256*FrameStitchnum);
P0 = 0;  
P1 = P0;  
% P2 = zeros(r,r);  
for k = 1:Batches
    ClutterData2(k,:) = ClutterData2(k,:);  
    P2 = P1+Qk;  
    Rk=cov(noise(k,:));
    Kk = P2*inv(P2+Rk);  
    ClutterData2(k+1,:) = ClutterData2(k,:)+Kk*(BandpassData(k,:)-ClutterData2(k,:));  
    P1 = (eye(1,1)-Kk)*P2;  
end  
PureData_KF=BandpassData-ClutterData2(2:size(ClutterData2,1),:);
% %%%%%%%%%%%%%%%%%%%Kalman Filter%%%%%%%%%%%%%%%%%%%%%%%
% 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%CT_Denoise%%%%%%%%%%%%%%%%%%%%%%%%
PureData_denoise=zeros(Batches,256*FrameStitchnum);
C1 = fdct_wrapping(PureData_KF,1,2);
E = cell(size(C1));
 for s=1:length(C1)
   E{s} = cell(size(C1{s}));
   for w=1:length(C1{s})
     A = C1{s}{w};
     E{s}{w} = median(abs(A(:) - median(A(:))))/.6745; 
   end
 end
Ct=C1;
Qt=C1;
 %对每个子带的变换系数做硬阈值处理
for s = 2:length(C1)
  thresh = 3*sigma + sigma*(s == length(C1));
  
%在阈值的选取上,是保留较大的系数,舍弃较小的系数, 因为根据Curvelet变换理论, 较大的Curvelet系数对应于较强的边缘,反之为噪声
  for w = 1:length(C1{s})
    Qt{s}{w} = C1{s}{w}.* (abs(C1{s}{w}) > thresh*E{s}{w});
  end
end
PureData_denoise=ifdct_wrapping(Qt,1);
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%CT_Denoise%%%%%%%%%%%%%%%%%%%%%%%%
% 
% %%%%%%%%%%%%%%%%modified CLEAN algorithm%%%%%%%%%%%%%%%%%
alphac=[];
PureData2=zeros(Batches,256*FrameStitchnum);

for d=1:1:256*FrameStitchnum
    alphac=[alphac,d];
end
for uu=1:Batches
    PureData2(uu,:)=PureData_denoise(uu,:).*alphac;
end
% %%%%%%%%%%%%%%%%%modified CLEAN algorithm%%%%%%%%%%%%%%%%%

% %%%%%%%%%%%%%%%%%%modified CLEAN algorithm%%%%%%%%%%%%%%%%%
template=importdata('C:\Users\mac\Desktop\files\matlabb\模板\Template.mat');
for i=1:Batches
    r1(i,:)=xcorr(PureData_denoise(i,:),template);
    r11(i,:)=r1(i,(length(PureData_denoise(i,:))-length(template)+1:length(r1(i,:))));
    r2(i,:)=r11(i,length(template):length(r11(i,:)));
end
PureData=r2;
NL=35;
NR=35;
%DirtyData=PowerData;
%[peaks,locs]=max(PureData(30,:));
mph1=100;
mph2=100;
mph3=100;

mpd=30;
%Adap=zeros(Batches,3);
%Adap=zeros(Batches,3,);
%figure;hold on;xlabel('thresholds');ylabel('row number');zlabel('peaks location');

spot1=cell(1,50);spot2=cell(1,50);spot3=cell(1,50);
for j=6:Batches
    [peaks,locs]=max(PureData(j,:));
    if peaks>0.1
%         mph1=0.55*peaks;
%         mph2=0.7*peaks;
%         mph3=0.9*peaks;
       mph1=0.6;
       mph2=0.65;
       mph3=0.7;
    end
    x=ones(1,Batches)*j;
    %[pks1,locs1]=findpeaks(PureData(j,:),'minpeakheight',mph1,'minpeakdistance',mpd); 
    DirtyData1=PureData(j,:);
    TOA1=[];
    k1=0;
    n1=0;
    for i=1:Iteration
        [val,loc]=max(DirtyData1);
        if loc>NL && loc<(256*FrameStitchnum-NR)
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
        if loc>NL && loc<(256*FrameStitchnum-NR)
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
        if loc>NL && loc<(256*FrameStitchnum-NR)
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
    people=0
end
    
%min
if min==mean1
    people=num1
    mph=mph1;
elseif min==mean2
    people=num2
    mph=mph2;
elseif min==mean3
    people=num3
    mph=mph3;
end



% spot1=cell(1,50);spot2=cell(1,50);spot3=cell(1,50);
% for j=6:Batches-5
%     [peaks,locs]=max(PureData(j,:));    
%     if peaks>0.1
% %         mph1=0.55*peaks;
% %         mph2=0.7*peaks;
% %         mph3=0.9*peaks;
%        mph1=0.7;
%        mph2=0.8;
%        mph3=0.9;
%        thre1=10;
%        thre2=10;
%        thre3=10;
%     end
%     x=ones(1,Batches)*j;
%     %[pks1,locs1]=findpeaks(PureData(j,:),'minpeakheight',mph1,'minpeakdistance',mpd); 
%     DirtyData1=PureData(j,:);
%     TOA1=[];
%     TOA11=[];
%     k1=0;
%     n1=0;
%     for i=1:Iteration
%         [val,loc]=max(DirtyData1);
%         if loc>NL && loc<(256*FrameStitchnum-NR)
%             if val>mph1
%             if val>max(PureData(j,loc-NL:loc-1)) && val>max(PureData(j,loc+1:loc+NR))
%                 k1=k1+1;
%                 TOA1=[TOA1,loc]
%             end
%             DirtyData1(loc-NL:loc+NR)=0;
%             i=i+1;
%             end
%         end
%     end 
%     for cc=1:size(TOA1,2)
%         loc=TOA1(cc);
%         if length(find(PureData(j:j+5,loc-10:loc+10)>mph1))>thre1
%               TOA11=[TOA11,loc]
%         end
%     end
%     %TOA1
%     x=ones(1,length(TOA11))*j;
%     y1=ones(1,length(TOA11))*mph1;
%     z1=zeros(1,length(TOA11));
%     for ii=1:length(TOA11)
%         z1(ii)=TOA11(ii);
%     end
%     spot1(j)={TOA11};
%     %plot3(y1,x,z1,'r.');
%     %[pks2,locs2]=findpeaks(PureData(j,:),'minpeakheight',mph2,'minpeakdistance',mpd);
%     DirtyData2=PureData(j,:);
%     TOA2=[];
%     TOA22=[];
%     k2=0;
%     n2=0;
%     for i=1:Iteration
%         [val,loc]=max(DirtyData2);
%         if loc>NL && loc<(256*FrameStitchnum-NR)
%             if val>mph2
%             if val>max(PureData(j,loc-NL:loc-1)) && val>max(PureData(j,loc+1:loc+NR))
%                 k2=k2+1;
%                 TOA2=[TOA2,loc];
%             end
%             DirtyData2(loc-NL:loc+NR)=0;
%             i=i+1;
%             end
%         end
%     end 
%     for cc=1:size(TOA2,2)
%         loc=TOA2(cc);
%         if length(find(PureData(j:j+5,loc-10:loc+10)>mph2))>thre2
%               TOA22=[TOA22,loc];
%         end
%     end
%     x=ones(1,length(TOA22))*j;
%     y2=ones(1,length(TOA22))*mph2;
%     z2=zeros(1,length(TOA22));
%     for ii=1:length(TOA22)
%         z2(ii)=TOA22(ii);
%     end
%     spot2(j)={TOA22};
% %     %plot3(y2,x,z2,'b.');
% %     [pks3,locs3]=findpeaks(PureData(j,:),'minpeakheight',mph3,'minpeakdistance',mpd);
%     DirtyData3=PureData(j,:);
%     TOA3=[];
%     TOA33=[];
%     k3=0;
%     n3=0;
%     for i=1:Iteration
%         [val,loc]=max(DirtyData1);
%         if loc>NL && loc<(256*FrameStitchnum-NR)
%             if val>mph3
%             if val>max(PureData(j,loc-NL:loc-1)) && val>max(PureData(j,loc+1:loc+NR))
%                 k3=k3+1;
%                 TOA3=[TOA3,loc];
%             end
%             DirtyData3(loc-NL:loc+NR)=0;
%             i=i+1;
%             end
%         end
%     end  
%     for cc=1:size(TOA3,2)
%         loc=TOA3(cc);
%         if length(find(PureData(j:j+5,loc-10:loc+10)>mph3))>thre3
%               TOA33=[TOA33,loc];
%         end
%     end 
%     x=ones(1,length(TOA33))*j;
%     y3=ones(1,length(TOA33))*mph3;
%     z3=zeros(1,length(TOA33));
%     for ii=1:length(TOA33)
%         z3(ii)=TOA33(ii);
%     end
%     spot3(j)={TOA33};
%     %plot3(y3,x,z3,'g.');
% end
% 
% sites1=[];num1=0;len1=[];
% sites2=[];num2=0;len2=[];
% sites3=[];num3=0;len3=[];
% for ii=1:Batches-5
%     temp1=cell2mat(spot1(ii));
%     temp2=cell2mat(spot2(ii));
%     temp3=cell2mat(spot3(ii));
%     num1=length(temp1);
%     num2=length(temp2);
%     num3=length(temp3);
%     len1=[len1,num1];
%     len2=[len2,num2];
%     len3=[len3,num3];
%     for jj=1:num1
%         sites1=[sites1;ii,temp1(jj)];
%     end
%     for jj=1:num2
%         sites2=[sites2;ii,temp2(jj)];
%     end
%     for jj=1:num3
%         sites3=[sites3;ii,temp3(jj)];
%     end
% end
% num1=fix(median(len1))
% num2=fix(median(len2))
% num3=fix(median(len3))
% var1=zeros(1,num1);
% var2=zeros(1,num2);
% var3=zeros(1,num3);
% % 
% if num1~=0
%     [Idx1, C1, sumD1, D1] = kmeans(sites1(:,2), num1);
%     for ii=1:num1
%     var1(ii)=std(sites1(Idx1==ii,2));
%     end
% end
% if num2~=0
%     [Idx2, C2, sumD2, D2] = kmeans(sites2(:,2), num2);
%     for ii=1:num2
%     var2(ii)=std(sites2(Idx2==ii,2));
%     end
% end
% if num3~=0
%     [Idx3, C3, sumD3, D3] = kmeans(sites3(:,2), num3);
%     for ii=1:num3
%     var3(ii)=std(sites3(Idx3==ii,2));
%     end
% end
% % %% Idx: 每个点所属的聚类标号
% % %% C: 每类的质心
% % %% numD: 1*K的和向量，存储的是类间所有点与该类质心点距离之和
% % %% D: N*K的矩阵，存储的是每个点与所有质心的距离
% % 
% % 
% % 
% mean1=mean(var1);
% mean2=mean(var2);
% mean3=mean(var3);
% min=0;
% if mean1~=0
%     min=mean1;
%     if min>mean2&&mean2~=0
%        min=mean2;
%     end
%     if min>mean3&&mean3~=0
%         min=mean3;
%     end
% end
% if num1==0&&num2==0&&num3==0
%     mph=mph1;
%     people=0;
% end
%     
% %min
% if min==mean1
%     people=num1;
%     mph=mph1;
% elseif min==mean2
%     people=num2;
%     mph=mph2;
% elseif min==mean3
%     people=num3;
%     mph=mph3;
% end