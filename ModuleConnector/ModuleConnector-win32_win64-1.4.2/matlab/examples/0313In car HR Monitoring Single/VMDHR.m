function [ measuredHeartbeat,energyofmodule]=VMDHR(HRsignal)
format long g
valueofk= [3,5,7,8,10,12,15,17,20,22,25,30,60];             %Kֵ�б仯���Ƿ�̶�һ��ֵ��ֻ�ֽ�һ��       ��������ԭ����   Сֵ�����Ҳ���   ��ֵ�����в���Ҫ��
Y = (-2^16/2:2^16/2-1)*(20)/2^16;
w=0;
dyy = [];
for Location=1          %!!!!!!!!!!!!!!!!!!!!!!!!                      %���ﵥ����Location��ֵ���Ե����õ�ĳ��λ�õĽ��
    
    flagheart = 0;   %�õ��������1
    
    
    DData = HRsignal;
%     figure
%     plot(HRsignal)
%     figure
%     fre=abs(fftshift(fft(HRsignal,2^16)))*1000;
%     plot(Y,fre);
    
    
%     BPF = load('Filter.mat');
%     DData=filter(BPF.Num,1,DData);
%     
%     figure
%     plot(DData)
%     xlabel('ʱ��');
%     ylabel('����');
%     figure
%     fre1=abs(fftshift(fft(DData,2^16)))*1000;
%     plot(Y,fre1);
%     
    for j=1:1:size(valueofk,2)                                    %��������VMD�ֽ��� valueofk�е�Kֵ��������
        
        if( flagheart == 0)                       %û���ҵ����ʺͺ������������K����VMD�ֽ�
%             K = valueofk(j);
            K=60;%15
            
            u = VMD_hb(DData,K);
            

            for i =1:K
                fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
                [resultvalue,result] = max(fre(i,:));
                provalue(i) = abs(Y(result)); 
%                 figure%�洢���зֽ����Ƶ��ֵ
%                 plot(Y,fre(i,:));
%     xlabel('Ƶ��/����');
%     ylabel('����');
                
            end
            aaaaaaaaaa=provalue*60;
            for i = 1:K
           
                
                if(   provalue(i) > 1.67  &&  provalue(i) < 2.5 )
                    
                    energyofu(i) = sum(u(i,:).*u(i,:));
                    w=w+1;
                    dyy = [dyy,provalue(i)];
                end%0.9-1.7 1.4-2.8
                   
                    
                    
                    flagheart = 1;
%                     K
                    
%                     break;
            end
                
             [energyofumax,energyofumaxi] = max(energyofu);  
             measuredHeartbeat(Location) = provalue(energyofumaxi);
            w
            provalue = [];
            energyofmodule=energyofumax;
        else
            break
        end
    end
    
    if (flagheart==0)
        measuredHeartbeat(Location) = -1;
    end
    provalue=[];
    
end

measuredHeartbeat=measuredHeartbeat.*60;
if (energyofmodule < 10^-9)
    measuredHeartbeat = 0;
end

% for i =1:K
%     figure
%     plot(u(i,:))                                           %�洢���зֽ����Ƶ��ֵ
%     
% end
% for i =1:K
%     figure                                            %�洢���зֽ����Ƶ��ֵ
%     plot(Y,fre(i,:))
% end



