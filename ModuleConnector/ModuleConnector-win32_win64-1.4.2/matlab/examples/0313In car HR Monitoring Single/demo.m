function heart = demo(Data)

    PureData = newfilter(  Data  );          %Ԥ���� ȥǰ50��ǰ50��

    [hrSignal,energyofrow] = maxEnergy(PureData(:,1:100));                    %ͨ�����������ѡ�ź�  1��50�У�ͨ����ͼ���ʵ��λ��ȷ���ķ�Χ
if energyofrow<11
   heart =0;
else
     heart = VMDHR(hrSignal);
end
% if energyofrow<11
%    heart =0;
% end
% 
