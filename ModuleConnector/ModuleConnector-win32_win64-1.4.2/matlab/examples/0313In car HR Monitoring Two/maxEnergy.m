function sig = maxEnergy(Pure)

Data = Pure;

for iLocation=1:size(Data,2)
    energyOfLocation(iLocation) = sum(Data(:,iLocation).*Data(:,iLocation));
end

dou = energyOfLocation;          %ȡ�� ĳ��λ�� ���ڷ�Χ�����п�ʱ���е�����
[energymax,energymaxi] = max(dou);                         %%ͨ����������ҵ������ź�
sig = Data(:,energymaxi);

% 
% figure
% plot((1:380)/20,sig)
% xlabel('Time/Seconds')
% ylabel('Amplitude')