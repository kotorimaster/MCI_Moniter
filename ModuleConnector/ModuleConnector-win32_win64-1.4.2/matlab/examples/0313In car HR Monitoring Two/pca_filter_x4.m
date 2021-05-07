function PureData=pca_filter_x4(RawData,rx_num,pg)
c=size(RawData);
FrameStitchnum=round(c(2)/156);
SpeedOfLight=3*10^8;
Resolution=0.006430041;
Fs=SpeedOfLight/(Resolution*2);

[bandfilter]=qfir_select(Fs,rx_num,pg);
Batches=c(1);
BandpassData=zeros(c);
ClutterData=zeros(c);
PureData=zeros(c);

firnum=50;
alpha=0.5;
%%%%Ԥ����%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for raw=1:1:Batches
    
    blockdata=RawData(raw,:);
    blockmean=mean(blockdata);
    DCmean=repmat(blockmean,1,length(blockdata));
    RawData(raw,:)=blockdata-DCmean;        %%%ȥ��ֱ������
    
    
    convres=conv(RawData(raw,:),bandfilter);
    BandpassData(raw,:)=convres(1,firnum/2+1:firnum/2+c(2));  %%%��ͨ�˲�
    if raw==1                                                               %%%ȥ���Ӳ�
        ClutterData(raw,:)=(1-alpha)*BandpassData(raw,:);
        PureData(raw,:)=BandpassData(raw,:)-ClutterData(raw,:);
    end
    if raw>1
        ClutterData(raw,:)=alpha*ClutterData(raw-1,:)+(1-alpha)*BandpassData(raw,:);
        PureData(raw,:)=BandpassData(raw,:)-ClutterData(raw,:);
    end
end
% %%%%%%%%%%%%%%%%%PCAȥ�Ӳ�%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% [U,S,V]=svd(BandpassData);
% E_total=sum(sum(S,1),2);
% % for i=1:min(size(S))
% %     if sum(sum(S(1:i,1:i),1),2)/E_total>0.85
% %         S(1:i,1:i)=0;break;
% %     end
% % end
% S(1,1)=0;
% PureData=U*S*V';
% % figure;
% % subplot(311);plot(BandpassData(1,:));title('ԭʼ�ز��ź�');
% % subplot(312);plot(PureData(1,:));title('PCAȥ�Ӳ�Ч��');
% % subplot(313);plot(PureData1(1,:));title('�Ӳ��˲���Ч��');

PureData=PureData(21:c(1),51:c(2));  %M=0;L=50;K=1;
