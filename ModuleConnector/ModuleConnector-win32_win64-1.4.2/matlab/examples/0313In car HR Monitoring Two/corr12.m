function [measuredHeartbeat]=corr12(RawData)

% M=0;L=50;K=1;
% pg=1;rx_num=2;
% PureData=pca_filter_x4(RawData,rx_num,pg,M,L,K);%�˲�

PureData = newfilter(RawData);

Data = PureData;
% rangeOfLocation = [33,64,136,139,150;
%                    80,111,183,186,197;];  %T 296-374     %����Ҫ��һ��


rangeOfLocation = [33,64;
                   80,111;];              %!!!!!!!!!!!!!!!!!!!!


valueofk= [3,5,8,15,20];             %Kֵ�б仯���Ƿ�̶�һ��ֵ��ֻ�ֽ�һ��       ��������ԭ����   Сֵ�����Ҳ���   ��ֵ�����в���Ҫ��

batch = size(RawData,1);

for Location = 1:2                     %!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    start=rangeOfLocation(1,Location);
    eend =rangeOfLocation(2,Location);
    
    for iLocation=start:eend
        energyOfLocation(iLocation,Location) = sum(Data(:,iLocation).*Data(:,iLocation));
    end
    dou = energyOfLocation(:,Location);          %ȡ�� ĳ��λ�� ���ڷ�Χ�����п�ʱ���е�����
    [energymax,energymaxi] = max(dou);                         %%ͨ����������ҵ������ź�
    DData = Data(:,energymaxi);
    
    if Location == 1
        
        flagbrea  = 0;   %�õ�����������1
        flagheart = 0;   %�õ��������1
        
        sigheart(Location,:) =zeros(1,batch);  %�洢���λ���Ϸֽ���������ź�
        
        for j=1:1:size(valueofk,2)                                    %��������VMD�ֽ��� valueofk�е�Kֵ��������
            
            provalue=[];                                              %�洢ÿ�εı�ѡֵ
            if(flagbrea == 0 || flagheart == 0)                       %û���ҵ����ʺͺ������������K����VMD�ֽ�
                K = valueofk(j);
                u = VMD_hb(DData,K);
                Y = [(-2^16/2:2^16/2-1)*(17)/2^16];
                
                
                for i =1:K
                    fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
                    [resultvalue,result] = max(fre(i,:));
                    provalue(i) = abs(Y(result));                                             %�洢���зֽ����Ƶ��ֵ
                    
                end
                
                for i = 1:K
                    if(   (  provalue(i)  >  2.0 )   ||         (     provalue(i) < 0.1   )     )          %ȥ������������Χ�ڵ�ֵ
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
        
        
        flagheart = 0;   %�õ��������1
        
        sigheart(Location,:) =zeros(1,batch);  %�洢���λ���Ϸֽ���������ź�
        
        
        
        
        
        
        provalue=[];
        K = 20;
        corrheart=zeros(K,1);                  %�洢�����������������
        
        u = VMD_hb(DData,K);
        Y = [(-2^16/2:2^16/2-1)*(17)/2^16];
        
        for i =1:K
            fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
            [resultvalue,result] = max(fre(i,:));
            provalue(i) = abs(Y(result));                                             %�洢���зֽ����Ƶ��ֵ
        end
        
        OOO=floor(provalue'*60)
        
        count=0;
        for i = 1:K
            
            corrheart(i)=min(min(corrcoef(u(i,:),sigheart(Location-1,:))));
            if(   (  provalue(i)  >  0.99 )   &&         (     provalue(i) < 2  )     )         %����K�����
                
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





