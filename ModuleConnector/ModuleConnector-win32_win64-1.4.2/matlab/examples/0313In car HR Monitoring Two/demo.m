function heart = demo(Data)

PureData = newfilter(  Data  );          %Ԥ���� ȥǰ50��ǰ50��
% figure(5)
% mesh(PureData)
% pause(0.1)
hrSignal = maxEnergy(PureData(:,1:50));                    %ͨ�����������ѡ�ź�  1��50�У�ͨ����ͼ���ʵ��λ��ȷ���ķ�Χ


heart(1) = VMDHR202(hrSignal);

[hrWave1,hrWave2] = Wave(PureData(:,50:100));
heart(2) = hrWave2;

