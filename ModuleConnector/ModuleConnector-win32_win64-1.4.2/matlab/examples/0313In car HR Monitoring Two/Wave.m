function [hrWave1,hrWave2] = Wave(PureData)
[r1_len]=location_multi_2(PureData);  %每一行能量最大的快时间位置
[hrWave1,hrWave2]=respiration_multi2(PureData,r1_len);

