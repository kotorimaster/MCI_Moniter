function [people]=counting627_1(RawData)
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
firnum=50;
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
         if raw==1
             ClutterData(raw,:)=(1-alpha)*BandpassData(raw,:);
             PureData(raw,:)=BandpassData(raw,:)-ClutterData(raw,:);
%              ClutterData1(raw,:)=(1-alpha)*BandpassData(raw,:).*wt; 
%              PureData1(raw,:)=BandpassData(raw,:)-ClutterData1(raw,:);
         end
         if raw>1
             ClutterData(raw,:)=alpha*ClutterData(raw-1,:)+(1-alpha)*BandpassData(raw,:);
             PureData(raw,:)=BandpassData(raw,:)-ClutterData(raw,:);
%              ClutterData1(raw,:)=alpha*ClutterData1(raw-1,:)+(1-alpha)*BandpassData(raw,:).*wt;
%              PureData1(raw,:)=BandpassData(raw,:)-ClutterData1(raw,:);
         end
%         PowerData(raw,:)=PureData(raw,:).^2;  

end

     
%PureData=PureData(6:size(PureData,1),:);
% x=0+5/1280:5/1280:5;
% plot(x,PureData(30,:));
% title('PureData');
% xlabel('x/[m]');
% ylabel('amplitude/[m]');
% drawnow;
% hold on;
% x=1:size(PureData,2);
% y=1:size(PureData,1);
% [X,Y]=meshgrid(x,y);
% %%z=pic(x,y);
% meshz(X,Y,PureData);
% x=0+5/1280:5/1280:5;
% plot(x,PureData(10,:));
% 
% axis([0 5 -1 1]);

% %hold on;
% drawnow;

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
%        mph1=0.15;
%        mph2=0.155;
%        mph3=0.16;
       mph1=0.22;
       mph2=0.21;
       mph3=0.2;
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
            if val>=max(PureData(j,loc-NL:loc-1)) && val>=max(PureData(j,loc+1:loc+NR))
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
            if val>=max(PureData(j,loc-NL:loc-1)) && val>=max(PureData(j,loc+1:loc+NR))
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
            if val>=max(PureData(j,loc-NL:loc-1)) && val>=max(PureData(j,loc+1:loc+NR))
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
% %% Idx: ÿ���������ľ�����
% %% C: ÿ�������
% %% numD: 1*K�ĺ��������洢����������е���������ĵ����֮��
% %% D: N*K�ľ��󣬴洢����ÿ�������������ĵľ���
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

