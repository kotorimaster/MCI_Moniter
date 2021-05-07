%%%%%%%%%%%十行的相关%%%%%%%%%%%
function [measuredRespiration, measuredHeartbeat]=heartbeat5(RawData)
M=0;L=50;K=1;
pg=1;rx_num=2;
PureData=pca_filter_x4(RawData,rx_num,pg,M,L,K);%滤波

rangeOfLocation = [87,156,284,286,314;
    164,232,360,363,391;];  %T 296-374

K=8;

measuredRespiration=[];
measuredHeartbeat=[];

batch = size(RawData,1);
zero=zeros(1,batch);
zerocorr=zeros(1,K*10);

for Location=1:1:5
    sigbrea(Location,:)  =zeros(1,batch);   %存储分解出的呼吸信号
    sigheart(Location,:) =zeros(1,batch);  %存储分解出的心跳信号
    
    measuredHeartbeat(Location) = 133;
    measuredRespiration(Location) = 66;
    
    provalue = [];
    preprovalue=[];
    
    corrbrea(Location,:)  = zerocorr;  %存储每次呼吸信号与其他做的相关
    corrheart(Location,:) = zerocorr; %存储每次心跳信号与其他做的相关
    
    
    allsignal=[]; %存储所有VMD分解出来的信号
    
    count=0;      %給相关计数
    
    start=rangeOfLocation(1,Location);
    eend=rangeOfLocation(2,Location);
    for iLocation=start:eend
        energyOfLocation(iLocation,Location) = sum(PureData(:,iLocation).*PureData(:,iLocation));
    end
    dou = energyOfLocation(:,Location);          %取出 某个位置 所在范围内所有快时间列的能量
    [energymax,energymaxi] = max(dou);                         %%通过能量最大找到所需信号
    
    DData = PureData(:,energymaxi-4:energymaxi+5);    %去除能量最大左右共十列信号
    
    
    
    
    
    for jj=1:10
        
        u = VMD_hb(DData(:,jj),K);
        Y = [(-2^16/2:2^16/2-1)*(49)/2^16];
        
        allsignal=[allsignal;u];                               %allsignal 最终会有5（K）*10=50行，每一行是一条信号
        
        if (Location > 1)
            for i=1:K;
                count=count+1;
                if(sigbrea(Location-1,:)~=zero)
                    corrbrea(Location,count)  = min(min(corrcoef(u(i,:),sigbrea(Location-1,:))));
                end
                if(sigheart(Location-1,:)~=zero)
                    corrheart(Location,count) = min(min(corrcoef(u(i,:),sigheart(Location-1,:))));
                end
            end
        end
        
        for i =1:K
            fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
            [resultvalue,result] = max(fre(i,:));
            preprovalue(i) = abs(Y(result));
        end
        preprovalue;
        provalue=[provalue preprovalue];
    end
    
    provalue=floor(provalue*100);
    lenprovalue = size(provalue,2);
    
    if (Location>1)                %去除相关
        for uuu=2:Location
            if (corrbrea(uuu,:)~=zerocorr)
                [mmm,nnn] = max(corrbrea(uuu,:));
                provalue(nnn)=-1;
            end
            if (corrheart(uuu,:)~=zerocorr)
                [mmm,nnn] = max(corrheart(uuu,:));
                provalue(nnn)=-1;
            end
        end
    end
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%找呼吸
    
    prebrea = provalue;
    for i = 1:lenprovalue
        if(prebrea(i) < 0.1*100  ||  prebrea(i) >1*100)
            prebrea(i)=-1;
        end
    end
    prebrea(prebrea==-1)=[];
    if(size(prebrea)~=0)
        table=tabulate(prebrea);
        [F,I]=max(table(:,2));
        I=find(table(:,2)==F);
        eee=table(I,1);
        measuredRespiration(Location) = eee(1);           %找到出现频次最大的频率作为呼吸
        [bream,brean]=find(provalue==measuredRespiration(Location));
        sigbrea(Location,:)=allsignal(brean(1),:);
    end
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%找心跳
    
    preheart = provalue;
    for i = 1:lenprovalue
        if(preheart(i) < 1*100  ||  preheart(i) >2.2*100)
            preheart(i)=-1;
        end
    end
    preheart(preheart==-1)=[];
    if(size(preheart)~=0)
        table=tabulate(preheart);
        [F,I]=max(table(:,2));
        I=find(table(:,2)==F);
        eee=table(I,1);
        measuredHeartbeat(Location) = eee(1);           %找到出现频次最大的频率作为心跳
        [heartm,heartn]=find(provalue==measuredHeartbeat(Location));
        sigheart(Location,:)=allsignal(heartn(1),:);
    end
    
   
end