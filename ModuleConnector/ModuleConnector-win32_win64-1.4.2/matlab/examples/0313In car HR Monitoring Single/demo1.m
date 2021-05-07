function heart = demo(Data)

PureData = newfilter(  Data  );          %预处理 去前50行前50列

[hrSignal,energyofrow] = maxEnergy(PureData(:,1:250));                    %通过最大能量挑选信号  1：50列，通过看图结合实际位置确定的范围

% [~,hrWave2] = Wave(PureData(:,50:100));
% heart = hrWave2;

 heart = extrfft(hrSignal);

if energyofrow<11
   heart =0;
end
