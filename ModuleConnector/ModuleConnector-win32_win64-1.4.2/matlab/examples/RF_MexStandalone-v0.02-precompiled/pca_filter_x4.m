function PureData=pca_filter_x4(RawData,rx_num,pg,M,L,K)
% RawData(:,1)=[];
c=size(RawData);
SpeedOfLight=3*10^8;
Resolution=0.006430041;
Fs=SpeedOfLight/(Resolution*2);

[bandfilter]=qfir_select(Fs,rx_num,pg);
Batches=c(1);
BandpassData=zeros(c);
PureData=zeros(c);

firnum=50;

%%%%预处理%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for raw=1:1:Batches
    blockdata=RawData(raw,:);
    blockmean=mean(blockdata);
    DCmean=repmat(blockmean,1,length(blockdata));
    RawData(raw,:)=blockdata-DCmean;
    
    convres=conv(RawData(raw,:),bandfilter);
    BandpassData(raw,:)=convres(1,firnum/2+1:firnum/2+c(2));  %%%带通滤波
    
end
%%%%%%%%%%%%%%%%%%PCA去杂波%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

[U,S,V] = svd(BandpassData);

PureData = BandpassData - U(:,:)*S(:,1:1)*V(:,1:1)';



PureData(:,1:20)=[];
