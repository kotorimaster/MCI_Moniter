function [ measuredHeartbeat]=VMDHR(HRsignal)
format long g
valueofk= [15,20,23,25];             %K值有变化，是否固定一个值，只分解一次       这样做的原因是   小值可能找不到   大值可能有不必要的
%valueofk= [7];
Y = (-2^16/2:2^16/2-1)*(20)/2^16;    %110HZ [-4,0,+4]--[30385,32769,35153]   2---33961
for Location=1          %!!!!!!!!!!!!!!!!!!!!!!!!                                         %这里单独给Location赋值可以单独得到某个位置的结果
    
    flagheart = 0;   %得到结果则置1
    
    
    DData = HRsignal;
    %     close all
    %     figure
    %     plot(HRsignal)
    %
    %     b=BPF(20,4,6);         %FPass = 4; FStop = 8;
    %     convres=conv(DData,b);
    %     DData=convres(26/2+1:26/2+size(DData,1));  %%%带通滤波
    
    %     figure
    %     plot(DData)
    
    
    for j=1:1:size(valueofk,2)                                    %经过几次VMD分解由 valueofk中的K值个数来定
        
        if( flagheart == 0)                       %没有找到心率和呼吸则继续增大K进行VMD分解
            K = valueofk(j);
            u = VMD_hb(DData,K);
            
            for i =1:K
                fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*10000;
                [resultvalue,result] = max(fre(i,:));
                provalue(i) = floor(abs(Y(result)) * 60);                                             %存储所有分解出的频率值
                %                                 [resultvalue,result] = max(fre(i,32769:39323));   %110Hz只在0 -- +2 Hz之间找
                %                                 provalue(i) = floor( abs(Y(result+32768))* 60  );                                             %存储所有分解出的频率值
                
                provalueEnergyRatio(i) = sum(fre(i,36045:39323).^2);   %1-2  /0-4
                maxmax(i) = resultvalue;
            end
            
            provalue;
            provalueEnergyRatio;
            %             for i = 1:K
            %                 figure
            %                 plot(Y,fre(i,:))
            %             end
            
            for i = 1:K
                if(   provalue(i) > 60 &&  provalue(i) < 100   )
  
                    measuredHeartbeat(Location) = provalue(i);
                    flagheart = 1;
                    
                    K;
                    break;
                end
            end
            
            provalue = [];
            provalueEnergyRatio = [];
        else
            break
        end
    end
    
    if (flagheart==0)
        measuredHeartbeat(Location) = -1;
    end
    provalue=[];
    
end

%  ff=abs(fftshift(fft(HRsignal,2^16)))*1000;
%  plot(Y,ff)







