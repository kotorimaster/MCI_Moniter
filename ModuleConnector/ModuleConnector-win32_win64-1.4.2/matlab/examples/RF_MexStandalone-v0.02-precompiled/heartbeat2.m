function [measuredRespiration, measuredHeartbeat]=heartbeat2(RawData,site)

M=0;L=50;K=1;
pg=1;rx_num=2;
PureData=pca_filter_x4(RawData,rx_num,pg,M,L,K);%�˲�
measuredRespiration = [0 0 0 0 0];
measuredHeartbeat = [0 0 0 0 0];
Data = PureData;
rangeOfLocation = [1,87,126,150,180;
    86,125,212,212,300;];  %T 296-374

valueofk= [3,5,8,15,20];             %Kֵ�б仯���Ƿ�̶�һ��ֵ��ֻ�ֽ�һ��       ��������ԭ����   Сֵ�����Ҳ���   ��ֵ�����в���Ҫ��

people=[];
countpeople=0;
for  iiiii=1:5
    if site(iiiii~=0)
        countpeople=countpeople+1;
        people(countpeople)=iiiii;
    end
end

for lllll=1:size(people,2)                                                      %���ﵥ����Location��ֵ���Ե����õ�ĳ��λ�õĽ��
    Location = people(lllll);
    flagbrea = 0;   %�õ�����������1
    flagheart = 0;
    %�õ��������1
    start=rangeOfLocation(1,Location);
    eend=rangeOfLocation(2,Location);
    
    for iLocation=start:eend
        energyOfLocation(iLocation,Location) = sum(Data(:,iLocation).*Data(:,iLocation));
    end
    dou = energyOfLocation(:,Location);          %ȡ�� ĳ��λ�� ���ڷ�Χ�����п�ʱ���е�����
    [energymax,energymaxi] = max(dou);                         %%ͨ����������ҵ������ź�
    DData = Data(:,energymaxi);
    
    for j=1:1:size(valueofk,2)                                    %��������VMD�ֽ��� valueofk�е�Kֵ��������
        
        if(flagbrea == 0 || flagheart == 0)                       %û���ҵ����ʺͺ������������K����VMD�ֽ�
            K = valueofk(j);
            u = VMD_hb(DData,K);
            Y = [(-2^16/2:2^16/2-1)*(40)/2^16];
            
            for i =1:K
                fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
                [resultvalue,result] = max(fre(i,:));
                provalue(i) = abs(Y(result));                                             %�洢���зֽ����Ƶ��ֵ
                
            end
            
            %provalue
            
            
            for i = 1:K
                if(   (  provalue(i)  >  1.8 )   ||         (     provalue(i) < 0.1   )     )          %ȥ������������Χ�ڵ�ֵ�Լ���һ��λ�õ����ֵ
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
                    if ( (flagheart == 1) && (    abs(provalue(i)-measuredHeartbeat(Location) ) < 0.05  )  )  %ȥ����������ֵ
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
                    if ( (flagbrea == 1) && (    abs(provalue(i)-measuredRespiration(Location) ) < 0.05  )  )  %ȥ�����κ���ֵ
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

