function heart = demo(Data)

PureData = newfilter(  Data  );          %Ԥ���� ȥǰ50��ǰ50��

[hrSignal,energyofrow] = maxEnergy(PureData(:,1:250));                    %ͨ�����������ѡ�ź�  1��50�У�ͨ����ͼ���ʵ��λ��ȷ���ķ�Χ

% [~,hrWave2] = Wave(PureData(:,50:100));
% heart = hrWave2;

 heart = extrfft(hrSignal);

if energyofrow<11
   heart =0;
end
