function PureData1=pca_filter_x4(RawData,rx_num,pg,M,L,K)
c=size(RawData);
% FrameStitchnum=round(c(2)/156);
FrameStitchnum=round(c(2)/78);
SpeedOfLight=3*10^8;
Resolution=0.006430041;
Fs=SpeedOfLight/(Resolution*2);

[bandfilter]=qfir_select(Fs,rx_num,pg);
Batches=c(1);
BandpassData=zeros(c);
ClutterData=zeros(c);
PureData1=zeros(c);
% pnum=76;
pnum=78;
firnum=50;
alpha=0.3;
%%%%Ԥ����%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for raw=1:1:Batches
    for framenum=1:FrameStitchnum
        blockdata=RawData(raw,(framenum-1)*pnum+1:min(framenum*pnum,c(2)));
%         min(framenum*pnum,c(2))
        blockmean=mean(blockdata);
        DCmean=repmat(blockmean,1,length(blockdata));
        RawData(raw,(framenum-1)*pnum+1:min(framenum*pnum,c(2)))=blockdata-DCmean;        %%%ȥ��ֱ������   
    end
 
        convres=conv(RawData(raw,:),bandfilter);
        BandpassData(raw,:)=convres(1,firnum/2+1:firnum/2+c(2));  %%%��ͨ�˲�  
        if raw==1                                                               %%%ȥ���Ӳ�
            ClutterData(raw,:)=(1-alpha)*BandpassData(raw,:);
            PureData1(raw,:)=BandpassData(raw,:)-ClutterData(raw,:);
        end
        if raw>1
            ClutterData(raw,:)=alpha*ClutterData(raw-1,:)+(1-alpha)*BandpassData(raw,:);
            PureData1(raw,:)=BandpassData(raw,:)-ClutterData(raw,:);
        end 
end
% %%%%%%%%%%%%%%%%%PCAȥ�Ӳ�%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[U,S,V]=svd(BandpassData);
E_total=sum(sum(S,1),2);
% for i=1:min(size(S))
%     if sum(sum(S(1:i,1:i),1),2)/E_total>0.85
%         S(1:i,1:i)=0;break;
%     end
% end
S(1,1)=0;
PureData2=U*S*V';
x=1/156:1/156:c(2)/156;
% figure;
% subplot(311);plot(x,BandpassData(10,:));title('ԭʼ�ز��ź�');xlabel('����/m');ylabel('��ֵ');
% subplot(312);plot(PureData2(10,:));title('PCAȥ�Ӳ�Ч��');
% subplot(313);plot(x,PureData1(10,:));title('�Ӳ��˲���Ч��');xlabel('����/m');ylabel('��ֵ');
PureData1=PureData1(M+1:c(1),L:c(2)-K);
% PureData1=PureData1(M+1:c(1),L:c(2)-K);
% X=size(PureData1,1);
% Y=size(PureData1,2);
% Zmax=max(max(PureData1));
% Zmin=min(min(PureData1));  
% x=[0:X-1];
% y=[0:Y-1];
% figure;
% mesh(y,x,PureData1); 
% axis([0 Y-1 0 X-1 Zmin Zmax]);%�޶���ʾ�ķ�Χ  
% xlabel('range');
% ylabel('time');
% zlabel('amplitude');
% title('PureData');

