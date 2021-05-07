function [measuredHeartbeat]=corr12(RawData)

% M=0;L=50;K=1;
% pg=1;rx_num=2;
% PureData=pca_filter_x4(RawData,rx_num,pg,M,L,K);%滤波

PureData = newfilter(RawData);

Data = PureData;
% rangeOfLocation = [33,64,136,139,150;
%                    80,111,183,186,197;];  %T 296-374     %这里要改一下


rangeOfLocation = [33,64;
                   80,111;];              %!!!!!!!!!!!!!!!!!!!!


valueofk= [3,5,8,15,20];             %K值有变化，是否固定一个值，只分解一次       这样做的原因是   小值可能找不到   大值可能有不必要的

batch = size(RawData,1);

for Location = 1:2                     %!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    start=rangeOfLocation(1,Location);
    eend =rangeOfLocation(2,Location);
    
    for iLocation=start:eend
        energyOfLocation(iLocation,Location) = sum(Data(:,iLocation).*Data(:,iLocation));
    end
    dou = energyOfLocation(:,Location);          %取出 某个位置 所在范围内所有快时间列的能量
    [energymax,energymaxi] = max(dou);                         %%通过能量最大找到所需信号
    DData = Data(:,energymaxi);
    
    if Location == 1
        
        flagbrea  = 0;   %得到呼吸率则置1
        flagheart = 0;   %得到结果则置1
        
        sigheart(Location,:) =zeros(1,batch);  %存储这个位置上分解出的心跳信号
        
        for j=1:1:size(valueofk,2)                                    %经过几次VMD分解由 valueofk中的K值个数来定
            
            provalue=[];                                              %存储每次的备选值
            if(flagbrea == 0 || flagheart == 0)                       %没有找到心率和呼吸则继续增大K进行VMD分解
                K = valueofk(j);
                u = VMD_hb(DData,K);
                Y = [(-2^16/2:2^16/2-1)*(17)/2^16];
                
                
                for i =1:K
                    fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
                    [resultvalue,result] = max(fre(i,:));
                    provalue(i) = abs(Y(result));                                             %存储所有分解出的频率值
                    
                end
                
                for i = 1:K
                    if(   (  provalue(i)  >  2.0 )   ||         (     provalue(i) < 0.1   )     )          %去掉不在正常范围内的值
                        provalue(i) = -1;
                    end
                end
                
                provalue
                
                if (flagbrea==0)
                    for i = 1:K
                        
                        if(   ( provalue(i)   > 0.1 )   &&   ( provalue(i)   < 0.7 )  )
                            measuredRespiration(Location) = provalue(i);
                            flagbrea=1;
                            break;
                        end
                        
                    end
                end
                
                
                if (flagheart==0)
                    for i = 1:K
                        if(   provalue(i) > 1  &&  provalue(i) < 2    )
                            measuredHeartbeat(Location) = provalue(i);
                            flagheart = 1;
                            sigheart(Location,:)=u(i,:);
                            break;
                        end
                        
                    end
                end
                
            end
        end
        
        
        if (flagheart==0)
            measuredHeartbeat(Location) = -1;
        end
        if (flagbrea==0)
            measuredRespiration(Location) = -1;
        end
        
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if Location==2
        
        
        flagheart = 0;   %得到结果则置1
        
        sigheart(Location,:) =zeros(1,batch);  %存储这个位置上分解出的心跳信号
        
        
        
        
        
        
        provalue=[];
        K = 20;
        corrheart=zeros(K,1);                  %存储与上条心跳做的相关
        
        u = VMD_hb(DData,K);
        Y = [(-2^16/2:2^16/2-1)*(17)/2^16];
        
        for i =1:K
            fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
            [resultvalue,result] = max(fre(i,:));
            provalue(i) = abs(Y(result));                                             %存储所有分解出的频率值
        end
        
        OOO=floor(provalue'*60)
        
        count=0;
        for i = 1:K
            
            corrheart(i)=min(min(corrcoef(u(i,:),sigheart(Location-1,:))));
            if(   (  provalue(i)  >  0.99 )   &&         (     provalue(i) < 2  )     )         %计算K个相关
                
                count = count+1;
                proprovalue(count) = provalue(i);
                corr(count) = corrheart(i);
                
            end
            
        end
        
        corrheart
        
        
        %         [minvalue,minsite] = min(abs(corr));
        %         measuredHeartbeat(Location) = proprovalue(minsite);
        
        if count >=2
            
            [maxvalue,maxsite] = max(abs(corr));
            proprovalue(maxsite) = -1;
            for eee = 1:1:count
                if proprovalue(eee) ~=-1 
                   measuredHeartbeat(Location) = proprovalue(eee); 
                   break;
                end
            end
        elseif count == 1
            
            measuredHeartbeat(Location) = proprovalue(1);
            
        elseif count == 0
            measuredHeartbeat(Location) = -1;
        end
        
        
        
    end
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    
end


measuredRespiration=measuredRespiration.*60;
measuredHeartbeat=measuredHeartbeat.*60;





