function [measuredRespiration, measuredHeartbeat]=heartbeat(RawData)

rangeOfLocation = [87,156,273,279,307;
    164,233,350,356,384;];  %T 296-374

abc=RawData;

Batches=size(RawData,1);
SpeedOfLight=3*10^8;
Resolution=0.00386751476861213;

Fs=SpeedOfLight/(Resolution*2);
[bandfilter]=qfir(Fs);
FrameStitchnum=size(RawData,2)/256;
BandpassData=zeros(Batches,256*FrameStitchnum);
ClutterData=zeros(Batches,256*FrameStitchnum);
PureData=zeros(Batches,256*FrameStitchnum);
% aanum=zeros(200,1);

pnum=256;
firnum=50;
alpha=0.5;
kesai=0.50;
flagbrea=0;

for raw=1:1:Batches
    for framenum=1:FrameStitchnum
        blockdata=RawData(raw,(framenum-1)*pnum+1:framenum*pnum);
        blockmean=mean(blockdata);
        DCmean=repmat(blockmean,1,pnum);
        RawData(raw,(framenum-1)*pnum+1:framenum*pnum)=blockdata-DCmean;                  %去直流
        
    end
    convres=conv(RawData(raw,:),bandfilter);
    BandpassData(raw,:)=convres(1,firnum/2+1:firnum/2+256*FrameStitchnum);
end

%PCA去杂波
s = svd(BandpassData);
[U,S,V] = svd(BandpassData);

%PCA去掉第一个主元矩阵
Data = BandpassData - U(:,:)*S(:,1:1)*V(:,1:1)';
quzabo = Data;


for Location=1:5
    flagbrea=0;
    flag = 0;
    start=rangeOfLocation(1,Location);
    eend=rangeOfLocation(2,Location);
    
    for iLocation=start:eend
        energyOfLocation(iLocation,Location) = sum(Data(:,iLocation).*Data(:,iLocation));
    end
    
    dou = energyOfLocation(:,Location);          %取出 某个位置 所在范围内所有快时间列的能量
    [energymax,energymaxi] = max(dou);                         %%通过能量最大找到所需信号
    DData = Data(:,energymaxi);
    
    
    
    
    K=3;
    
    
    u = VMD_hb(DData,K);
    
    Y = [(-2^16/2:2^16/2-1)*(40)/2^16];
    for i =1:K
        fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
        [resultvalue,result] = max(fre(i,:));
        proHeartbeat(i) = abs(Y(result));
        
    end
    
    
%     proHeartbeat
%     measuredRespiration = zeros(1,5);
    if (flagbrea==0)
        for i = 1:K
            if(   ( proHeartbeat(i)   > 0.1 )   &&   ( proHeartbeat(i)   < 1.7 )  )
                
                measuredRespiration(Location) = proHeartbeat(i);
                flagbrea=1;
                break;
            end
            
        end
    end
    
    for i = 1:K
        if(   ( abs(   proHeartbeat(i)-measuredRespiration(Location)  )   <0.05  )         ||    ( proHeartbeat(i)>1.7  )   )
            proHeartbeat(i) = -1;
        end
        if Location>1
            if (  abs(   proHeartbeat(i)-measuredRespiration(Location-1)  )   <0.05      ||   abs(   proHeartbeat(i)-measuredHeartbeat(Location-1)  )  )
                proHeartbeat(i) = -1;
            end
        end
    end
    
%     proHeartbeat
    
    for i = 1:K
        if(   proHeartbeat(i) > 0.9  &&  proHeartbeat(i) <1.7     )
            measuredHeartbeat(Location) = proHeartbeat(i);
            flag = 1;
%             K
            break;
            
        end
        
    end
    
    
    if(flag==0)
        
        K=5;
        u = VMD_hb(DData,K);
        
        
        for i =1:K
            fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
            [resultvalue,result] = max(fre(i,:));
            proHeartbeat(i) = abs(Y(result));
            
        end
%         proHeartbeat
        
        
        if (flagbrea==0)
            for i = 1:K
                if(   ( proHeartbeat(i)   > 0.1 )   &&   ( proHeartbeat(i)   < 1.7 )  )
                    
                    measuredRespiration(Location) = proHeartbeat(i);
                    flagbrea=1;
                    break;
                end
                
            end
        end
        
        for i = 1:K
            if(   ( abs(   proHeartbeat(i)-measuredRespiration(Location)  )   <0.05  )         ||    ( proHeartbeat(i)>1.8  )   )
                proHeartbeat(i) = -1;
            end
            if Location>1
                if (  abs(   proHeartbeat(i)-measuredRespiration(Location-1)  )   <0.05      ||   abs(   proHeartbeat(i)-measuredHeartbeat(Location-1)  )  )
                    proHeartbeat(i) = -1;
                end
            end
        end
%         proHeartbeat
        for i = 1:K
            if(   proHeartbeat(i) > 0.9  &&proHeartbeat(i) <1.7     )
                measuredHeartbeat(Location) = proHeartbeat(i);
                flag = 1;
%                 K
                break;
                
            end
            
        end
    end
    
    if(flag == 0)
        K=15;
        u = VMD_hb(DData,K);
        
        for i =1:K
            fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
            [resultvalue,result] = max(fre(i,:));
            proHeartbeat(i) = abs(Y(result));
            
        end
%         proHeartbeat
        
        if (flagbrea==0)
            for i = 1:K
                if(   ( proHeartbeat(i)   > 0.1 )   &&   ( proHeartbeat(i)   < 1.7 )  )
                    
                    measuredRespiration(Location) = proHeartbeat(i);
                    flagbrea=1;
                    break;
                end
                
            end
        end
        
        for i = 1:K
            if(   ( abs(   proHeartbeat(i)-measuredRespiration(Location)  )   <0.05  )         ||    ( proHeartbeat(i)>1.8  )   )
                proHeartbeat(i) = -1;
            end
            if Location>1
                if (  abs(   proHeartbeat(i)-measuredRespiration(Location-1)  )   <0.05      ||   abs(   proHeartbeat(i)-measuredHeartbeat(Location-1)  )<0.05  )
                    proHeartbeat(i) = -1;
                end
            end
        end
%         proHeartbeat
        for i = 1:K
            if(   proHeartbeat(i) > 0.9  &&proHeartbeat(i) <1.7    )
                measuredHeartbeat(Location) = proHeartbeat(i);
                flag = 1;
%                 K
                break;
                
            end
            
        end
    end
    
    if(flag == 0)
        
        K=20;
        u = VMD_hb(DData,K);
        
        for i =1:K
            fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
            [resultvalue,result] = max(fre(i,:));
            proHeartbeat(i) = abs(Y(result));
            
        end
%         proHeartbeat
        
        
        if (flagbrea==0)
            for i = 1:K
                if(   ( proHeartbeat(i)   > 0.1 )   &&   ( proHeartbeat(i)   < 1.7 )  )
                    
                    measuredRespiration(Location) = proHeartbeat(i);
                    flagbrea=1;
                    break;
                end
                
            end
        end
        
        for i = 1:K
            if(   ( abs(   proHeartbeat(i)-measuredRespiration(Location)  )   <0.05  )         ||    ( proHeartbeat(i)>1.8  )   )
                proHeartbeat(i) = -1;
            end
            if Location>1
                if (  abs(   proHeartbeat(i)-measuredRespiration(Location-1)  )   <0.05      ||   abs(   proHeartbeat(i)-measuredHeartbeat(Location-1)  )  )
                    proHeartbeat(i) = -1;
                end
            end
        end
%         proHeartbeat
        for i = 1:K
            if(   proHeartbeat(i) > 0.9  &&proHeartbeat(i) <1.7   )
                measuredHeartbeat(Location) = proHeartbeat(i);
                flag = 1;
%                 K
                break;
            end
            
        end
    end
    if (flag==0)
        measuredHeartbeat(Location) = 1.3252;
    end
    if (flagbrea==0)
        measuredRespiration(Location) = 0.6666;
    end
    proHeartbeat=[];
end

% bre1 = measuredRespiration(1);
% bre2 = measuredRespiration(2);
% bre3 = measuredRespiration(3);
% bre4 = measuredRespiration(4);
% bre5 = measuredRespiration(5);
% h1 =   measuredHeartbeat(1);
% h2 =   measuredHeartbeat(2);
% h3 =   measuredHeartbeat(3);
% h4 =   measuredHeartbeat(4);
% h5 =   measuredHeartbeat(5);



