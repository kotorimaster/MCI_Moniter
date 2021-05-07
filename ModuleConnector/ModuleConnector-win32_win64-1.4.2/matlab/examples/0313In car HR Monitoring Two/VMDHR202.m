function [ measuredHeartbeat]=VMDHR(HRsignal)
format long g
valueofk= [15,20,23,25];             %Kֵ�б仯���Ƿ�̶�һ��ֵ��ֻ�ֽ�һ��       ��������ԭ����   Сֵ�����Ҳ���   ��ֵ�����в���Ҫ��
%valueofk= [7];
Y = (-2^16/2:2^16/2-1)*(20)/2^16;    %110HZ [-4,0,+4]--[30385,32769,35153]   2---33961
for Location=1          %!!!!!!!!!!!!!!!!!!!!!!!!                                         %���ﵥ����Location��ֵ���Ե����õ�ĳ��λ�õĽ��
    
    flagheart = 0;   %�õ��������1
    
    
    DData = HRsignal;
    %     close all
    %     figure
    %     plot(HRsignal)
    %
    %     b=BPF(20,4,6);         %FPass = 4; FStop = 8;
    %     convres=conv(DData,b);
    %     DData=convres(26/2+1:26/2+size(DData,1));  %%%��ͨ�˲�
    
    %     figure
    %     plot(DData)
    
    
    for j=1:1:size(valueofk,2)                                    %��������VMD�ֽ��� valueofk�е�Kֵ��������
        
        if( flagheart == 0)                       %û���ҵ����ʺͺ������������K����VMD�ֽ�
            K = valueofk(j);
            u = VMD_hb(DData,K);
            
            for i =1:K
                fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*10000;
                [resultvalue,result] = max(fre(i,:));
                provalue(i) = floor(abs(Y(result)) * 60);                                             %�洢���зֽ����Ƶ��ֵ
                %                                 [resultvalue,result] = max(fre(i,32769:39323));   %110Hzֻ��0 -- +2 Hz֮����
                %                                 provalue(i) = floor( abs(Y(result+32768))* 60  );                                             %�洢���зֽ����Ƶ��ֵ
                
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







