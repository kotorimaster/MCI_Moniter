function heart = demo(Data)

    PureData = newfilter(  Data  );          %预处理 去前50行前50列

    [hrSignal,energyofrow] = maxEnergy(PureData(:,1:100));                    %通过最大能量挑选信号  1：50列，通过看图结合实际位置确定的范围
if energyofrow<11
   heart =0;
else
     heart = VMDHR(hrSignal);
end
% if energyofrow<11
%    heart =0;
% end
% 
