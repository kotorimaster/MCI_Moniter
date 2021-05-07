function [pp,PureData_svd1]=che_countless(RawData,xiu)
tic
FrameStitchnum=3;
SpeedOfLight=3*10^8;
Resolution=1/256;
Fs=SpeedOfLight/(Resolution*2);
[bandfilter]=qfir(Fs);
%Receive Raw Data
Batches=200;
pnum=256;
firnum=100;
people=0;
smean1=zeros(1,200);
smean2=zeros(1,200);
stdmean1=zeros(1,200);
stdmean2=zeros(1,200);
stdmmean1=zeros(1,200);
stdmmean2=zeros(1,200);
    
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
    [U,S,V]=svd(BandpassData);
    S1=zeros(size(S));
    S1(2,2)=S(2,2);
    PureData_svd1=U*S1*V';
for nn = 1:Batches
    sum1=sum(PureData_svd1(:,1:200),2);
    sum2=sum(PureData_svd1(:,205:400),2);
    smean1(1,nn)=mean(sum1);
    smean2(1,nn)=mean(sum2);
    %行(快时间)标准差
    std1=std(PureData_svd1(11:end,1:200),0,2);
    std2=std(PureData_svd1(11:end,205:400),0,2);
    stdmean1(1,nn)=mean(std1);
    stdmean2(1,nn)=mean(std2);
    %列(慢时间)标准差
    stdm1=std(PureData_svd1(11:end,1:200),0,1);
    stdm2=std(PureData_svd1(11:end,205:400),0,1);
    stdmmean1(1,nn)=mean(stdm1);
    stdmmean2(1,nn)=mean(stdm2);
end
sum1e=mean(smean1);
sum2e=mean(smean2);
std1e=mean(stdmean1);
std2e=mean(stdmean2);
stdm1e=mean(stdmmean1);
stdm2e=mean(stdmmean2);  
input_my=[sum1e sum2e std1e std2e stdm1e stdm2e];
people = classRF_predict_xiu(input_my,xiu);
% varia = [varia people1]
if people == 0
    pp = [0 0 0 0 0];
elseif people == 1
    pp = [1 0 0 0 0];
elseif people == 2
    pp = [0 1 0 0 0];
elseif people == 3
    pp = [0 0 1 0 0];
elseif people == 4
    pp = [0 0 0 1 0];
elseif people == 5
    pp = [0 0 0 0 1];
elseif people == 6
    pp = [1 1 0 0 0];
elseif people == 7
    pp = [1 0 1 0 0];
elseif people == 8
    pp = [1 0 0 1 0];
elseif people == 9
    pp = [1 0 0 0 1];
elseif people == 10
    pp = [1 1 1 0 0];
elseif people == 11
    pp = [1 1 0 1 0];
elseif people == 12
    pp = [1 1 0 0 1];
elseif people == 13
    pp = [1 0 1 1 0];
elseif people == 14
    pp = [1 0 1 0 1];
elseif people == 15
    pp = [1 0 0 1 1];
% end
elseif people == 16
    pp = [1 1 1 1 0];
elseif people == 17
    pp = [1 1 1 0 1]; 
elseif people == 18
    pp = [1 1 0 1 1];
elseif people == 19
    pp = [1 0 1 1 1];
elseif people == 20
    pp = [1 1 1 1 1];
end   

end
%  people = mode(varia)


% toc