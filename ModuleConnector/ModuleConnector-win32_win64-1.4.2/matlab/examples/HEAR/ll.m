
clc
clear
close all

RawData = load('C:\Users\YooMooY\Desktop\2018-11-06-15-46-13.txt');
RawData(:,1)=[];


for i =1 :1 : 60
    Data=RawData(   (i-1)*300+1   :  i*300    ,:);
    
    
    i
    PureData=newfilter(Data);
    
    [br_s,hbradar1]=respiration_multi2_vncmd(PureData);   %%% VNCMD
    
    [radar(i,:)] = hbradar1
    
end


