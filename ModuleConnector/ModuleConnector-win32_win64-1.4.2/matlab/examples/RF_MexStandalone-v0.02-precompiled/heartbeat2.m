function [measuredRespiration, measuredHeartbeat]=heartbeat2(RawData,site)

M=0;L=50;K=1;
pg=1;rx_num=2;
PureData=pca_filter_x4(RawData,rx_num,pg,M,L,K);%滤波
measuredRespiration = [0 0 0 0 0];
measuredHeartbeat = [0 0 0 0 0];
Data = PureData;
rangeOfLocation = [1,87,126,150,180;
    86,125,212,212,300;];  %T 296-374

valueofk= [3,5,8,15,20];             %K值有变化，是否固定一个值，只分解一次       这样做的原因是   小值可能找不到   大值可能有不必要的

people=[];
countpeople=0;
for  iiiii=1:5
    if site(iiiii~=0)
        countpeople=countpeople+1;
        people(countpeople)=iiiii;
    end
end

for lllll=1:size(people,2)                                                      %这里单独给Location赋值可以单独得到某个位置的结果
    Location = people(lllll);
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
    
    for j=1:1:size(valueofk,2)                                    %经过几次VMD分解由 valueofk中的K值个数来定
        
        if(flagbrea == 0 || flagheart == 0)                       %没有找到心率和呼吸则继续增大K进行VMD分解
            K = valueofk(j);
            u = VMD_hb(DData,K);
            Y = [(-2^16/2:2^16/2-1)*(40)/2^16];
            
            for i =1:K
                fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
                [resultvalue,result] = max(fre(i,:));
                provalue(i) = abs(Y(result));                                             %存储所有分解出的频率值
                
            end
            
            %provalue
            
            
            for i = 1:K
                if(   (  provalue(i)  >  1.8 )   ||         (     provalue(i) < 0.1   )     )          %去掉不在正常范围内的值以及上一个位置的相近值
                    provalue(i) = -1;
                end
                if Location>1
                    lalala=provalue(i);
                    lalala1=measuredRespiration(Location-1);
                    lalala2=measuredHeartbeat(Location-1);
                    lalala3=abs(   provalue(i)-measuredRespiration(Location-1)  );
                    lalala4=abs(   provalue(i)-measuredHeartbeat(Location-1)  );
                    if (  abs( provalue(i)-measuredRespiration(Location-1) )<0.05 || abs( provalue(i)-measuredHeartbeat(Location-1))< 0.05  )
                        provalue(i) = -1;
                    end
                end
            end
            
            %provalue
            
            if (flagbrea==0)
                for i = 1:K
                    if ( (flagheart == 1) && (    abs(provalue(i)-measuredHeartbeat(Location) ) < 0.05  )  )  %去掉本次心跳值
                        provalue(i)=-1;
                    end
                    if(   ( provalue(i)   > 0.1 )   &&   ( provalue(i)   < 1 )  )
                        measuredRespiration(Location) = provalue(i);
                        flagbrea=1;
                        break;
                    end
                    
                end
            end
            
            % measuredRespiration
            
            if (flagheart==0)
                for i = 1:K
                    if ( (flagbrea == 1) && (    abs(provalue(i)-measuredRespiration(Location) ) < 0.05  )  )  %去掉本次呼吸值
                        provalue(i)=-1;
                    end
                    if(   provalue(i) > 1  &&  provalue(i) < 2.2    )
                        measuredHeartbeat(Location) = provalue(i);
                        flagheart = 1;
                        %K
                        break;
                        
                    end
                    
                end
            end
            %measuredHeartbeat
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



measuredRespiration=measuredRespiration.*100;
measuredHeartbeat=measuredHeartbeat.*100;



% toc

