function [time_1, value_1,time_2, value_2] = oxi_yandiansai()
[time_1, value_1]=textread('oxi1_data_matlab.txt','%n %f');
[time_2, value_2]=textread('oxi2_data_matlab.txt','%n %f');
