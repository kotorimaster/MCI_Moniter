function [measuredRespiration, measuredHeartbeat]=heartbeat(RawData)

rangeOfLocation = [99,156,284,286,314;
    176,232,360,363,391;];  %T 296-374




valueofk= [3,5,8,15,20];
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
aanum=zeros(200,1);

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
measuredRespiration=[];
measuredHeartbeat=[];

for Location=1:5
    flagbrea = 0;   %得到呼吸率则置1
    flagheart = 0;
       %得到结果则置1
    start=rangeOfLocation(1,Location);
    eend=rangeOfLocation(2,Location);
    for iLocation=start:eend
        energyOfLocation(iLocation,Location) = sum(Data(:,iLocation).*Data(:,iLocation));
    end
    dou = energyOfLocation(:,Location);          %取出 某个位置 所在范围内所有快时间列的能量
    [energymax,energymaxi] = max(dou);                         %%通过能量最大找到所需信号
    DData = Data(:,energymaxi);
    
    for j=1:1:size(valueofk,2)
        
        if(flagbrea == 0 || flagheart == 0)
            K = valueofk(j);
            u = VMD_hb(DData,K);
            Y = [(-2^16/2:2^16/2-1)*(40)/2^16];
            
            for i =1:K
                fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
                [resultvalue,result] = max(fre(i,:));
                provalue(i) = abs(Y(result));
                
            end
            
%             provalue
            
            
            for i = 1:K
                if(   (  provalue(i)  >  1.8 )   ||         (     provalue(i) < 0.1   )     )
                    provalue(i) = -1;
                end
                if Location>1
                    lalala=provalue(i);
                    lalala1=measuredRespiration(Location-1);
                    lalala2=measuredHeartbeat(Location-1);
                    lalala3=abs(   provalue(i)-measuredRespiration(Location-1)  );
                    lalala4=abs(   provalue(i)-measuredHeartbeat(Location-1)  );
                    if (  abs( provalue(i)-measuredRespiration(Location-1) )<0.05 || abs( provalue(i)-measuredHeartbeat(Location-1))< 0.01  )
                        provalue(i) = -1;
                    end
                end
            end
            
%             provalue
            
            if (flagbrea==0)
                for i = 1:K
                    if ( (flagheart == 1) && (    abs(provalue(i)-measuredHeartbeat(Location) ) < 0.05  )  )
                        provalue(i)=-1;
                    end
                    if(   ( provalue(i)   > 0.1 )   &&   ( provalue(i)   < 1.2 )  )
                        
                        measuredRespiration(Location) = provalue(i);
                        flagbrea=1;
                        break;
                    end
                    
                end
            end
            
%             measuredRespiration
            
            if (flagheart==0)
                for i = 1:K
                    if ( (flagbrea == 1) && (    abs(provalue(i)-measuredRespiration(Location) ) < 0.05  )  )
                        provalue(i)=-1;
                    end
                    if(   provalue(i) > 0.9  &&  provalue(i) <1.8     )
                        measuredHeartbeat(Location) = provalue(i);
                        flagheart = 1;
%                         K
                        break;
                        
                    end
                    
                end
            end
%             measuredHeartbeat
        end
    end
    
    
    if (flagheart==0)
        measuredHeartbeat(Location) = 1.3333;
    end
    if (flagbrea==0)
        measuredRespiration(Location) = 0.6666;
    end
    provalue=[];
    
    
end

% measuredRespiration
% measuredHeartbeat



toc

