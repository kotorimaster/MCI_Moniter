function heart = demo(Data)

PureData = newfilter(  Data  );          %预处理 去前50行前50列
% figure(5)
% mesh(PureData)
% pause(0.1)
hrSignal = maxEnergy(PureData(:,1:50));                    %通过最大能量挑选信号  1：50列，通过看图结合实际位置确定的范围


heart(1) = VMDHR202(hrSignal);

[hrWave1,hrWave2] = Wave(PureData(:,50:100));
heart(2) = hrWave2;

