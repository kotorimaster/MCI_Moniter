function [position, PureData]=fcounting(RawData,batch)

% count=zeros(1,5);%1-5人
position=zeros(1,6);%1-5号+t

thres1=1;
thres2=0.12;
thres3=0.25;
thres4=0.5;
thres5=0.29;

FrameStitchnum=3;
SpeedOfLight=3*10^8;
Resolution=0.00386751476861213;
Fs=SpeedOfLight/(Resolution*2);
[bandfilter]=qfir(Fs);
pnum=256;
firnum=100;
BandpassData=zeros(batch,256*FrameStitchnum);
for raw=1:1:batch
    for framenum=1:FrameStitchnum
        blockdata=RawData(raw,(framenum-1)*pnum+1:framenum*pnum);
        blockmean=mean(blockdata);
        DCmean=repmat(blockmean,1,pnum);
        RawData(raw,(framenum-1)*pnum+1:framenum*pnum)=blockdata-DCmean;
    end
        convres=conv(RawData(raw,:),bandfilter);
        BandpassData(raw,:)=convres(1,firnum/2+1:firnum/2+256*FrameStitchnum);
end
%%%%%%%%%%%%%%%%%%%%%%SVD--new%%%%%%%%%%%%%%%%%%%%%%%%%%%
[U,S,V]=svd(BandpassData);
S1=zeros(size(S));
S1(2,2)=S(2,2);
PureData=U*S1*V';
%%%%%%%%%%%%%%%%%%%%%%SVD--new%%%%%%%%%%%%%%%%%%%%%%%%%%%

PureData_svd=abs(PureData);
chip1=PureData_svd(:,1:55);
chip2=PureData_svd(:,56:130);
chip3=PureData_svd(:,245:263);
chip4=PureData_svd(:,220:244);
chip5=PureData_svd(:,264:300);
%幅值和
sum1=sum(PureData_svd(:,1:200),2);
sum2=sum(PureData_svd(:,205:400),2);
sum1=mean(sum1);
sum2=mean(sum2);

%行(快时间)标准差
% std1=std(PureData_svd(:,1:200),0,2);
std2=std(PureData_svd(:,205:400),0,2);
% std1=mean(std1);
std2=mean(std2);

if sum1>0.9 ||sum2>1%是否有人
%     th=max(max(PureData_svd(:,101:160)));
    if sum1>300 && sum2>80 %5人
%         count(1,5)=count(1,5)+1;
        position(1,1:5)=ones(1,5);
        
    elseif sum1<=15 %2/3/4/5有1人
        for i=1:100
            temp=zeros(1,5);
            loctemp=[];
            temp(1,2)=max(chip2(i,:))-thres2;
            temp(1,3)=max(chip3(i,:))-thres3;
            temp(1,4)=max(chip4(i,:))-thres4;
            temp(1,5)=max(chip5(i,:))-thres5;
            [val,loc]=max(temp);
            if val>0
                loctemp=[loctemp,loc];
            end
        end
        if ~isempty(loctemp)
            position(1,mode(loctemp))=1;
        end
   
%     elseif sum1<90 && sum2<30 && th<1.5 %1号/有2人/躺1人
%         if max(max(PureData_svd(:,205:400)))>0.9&&std1<0.25 %躺1人
%             %count(1,1)=count(1,1)+1;
%             position(1,6)=1;
%         else
%             position(1,1)=1;
%             postemp=zeros(1,5);
%             for i=1:100
%                 if max(chip2(i,:))>thres2&&sum1>57.5
%                     %count(1,2)=count(1,2)+1;
%                     postemp(1,2)=postemp(1,2)+1;
%                 end
%                 if max(chip1(i,:))>2
%                     postemp(1,3)=postemp(1,3)+1;
%                 end
%                 if max(chip4(i,:))>0.2
%                     postemp(1,4)=postemp(1,4)+1;
%                 end
%                 if max(chip5(i,:))>thres5
%                     postemp(1,5)=postemp(1,5)+1;
%                 end
%             end
%             [~,loc]=max(postemp);
%             position(1,loc)=1;
%         end
    
    elseif sum1<70&&sum2>120&&std2>0.9 %3,4,5有3人
        %count(1,3)=count(1,3)+1;
        position(1,3:5)=ones(1,3);
    
%     elseif std1<0.6 && std2<0.32 %躺1人+1/1,2
%         %count(1,2)=count(1,2)+1;
%         position(1,6)=1;
%         position(1,1)=1;
%         if sum1<=125
%             %count(1,2)=count(1,2)-1;
%             %count(1,3)=count(1,3)+1;
%             position(1,2)=1;
%         end
        
    else
        if max(max(chip1))>thres1
            position(1,1)=1;
        end
        if max(max(chip2))>thres2
            position(1,2)=1;
        end
        if max(max(chip3))>thres3
            position(1,3)=1;
        end
        if max(max(chip4))>thres4
            position(1,4)=1;
        end
        if max(max(chip5))>thres5
            position(1,5)=1;
        end
%         postemp=zeros(1,5);
%         for i=1:100
%             temp=zeros(1,5);
%             temp(1,1)=max(chip1(i,:));
%             temp(1,2)=max(chip2(i,:));
%             temp(1,3)=max(chip3(i,:));
%             temp(1,4)=max(chip4(i,:));
%             temp(1,5)=max(chip5(i,:));
%             for x=1:4
%                 [val,loc]=max(temp);
%                 if val>0.2
%                     postemp(1,loc)=postemp(1,loc)+1;
%                     temp(1,loc)=0;
%                 end
%             end
%         end
%         for x=1:4
%         [~,loc]=max(postemp);
%         position(1,loc)=1;
%         end
    end
end
