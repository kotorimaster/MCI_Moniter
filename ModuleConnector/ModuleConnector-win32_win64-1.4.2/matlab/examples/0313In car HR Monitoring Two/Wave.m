function [hrWave1,hrWave2] = Wave(PureData)
[r1_len]=location_multi_2(PureData);  %ÿһ���������Ŀ�ʱ��λ��
[hrWave1,hrWave2]=respiration_multi2(PureData,r1_len);

