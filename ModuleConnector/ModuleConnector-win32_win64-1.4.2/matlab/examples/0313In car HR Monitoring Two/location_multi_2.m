%% time delay by cross correlation
%%æ‹?‰„@‹’¼—¬•ª—ÊA?’Ê?”gA?”g
% RawData=load('C:\Users\Wenfeng\Desktop\RawData\static\2016-07-08-20-46-53.txt');
function [r1_len,r2_len]=location_multi(Pure)
% RawData=load('F:\ProData\cl\static\1\radar\2016-07-15-21-39-28.txt');

c=size(Pure);
valueplace=zeros(c(1),1);
for ii=1:c(1)
    [maxvalue,valueplace(ii)]=max(Pure(ii,:));
end
% r1_len=fix(median(valueplace))+L+fix(0.1794*pnum)
r1_len=valueplace;
end
