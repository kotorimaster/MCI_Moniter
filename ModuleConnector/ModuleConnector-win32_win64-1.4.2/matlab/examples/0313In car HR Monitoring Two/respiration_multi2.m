%% time delay by cross correlation
%%愭嫀?墑岪嫀捈棳暘検丄?捠?攇丄?攇
% RawData=load('C:\Users\Wenfeng\Desktop\RawData\static\2016-07-08-20-46-53.txt');
function [hr_s1,hr_s2]=respiration_multi2(Pure,r1_len)  %1能量最大 2频次最多
% RawData=load('F:\ProData\cl\static\1\radar\2016-07-15-21-39-28.txt');
Sig=zeros(1,size(Pure,1));
for i=1:size(Pure,1)
    Sig(i)=Pure(i,r1_len(i));
end

Fs1=20;
w1=0.1/(Fs1/2);w2=1.8/(Fs1/2);
[a,b]=butter(5,[w1 w2],'bandpass');
Sig=filter(a,b,Sig);
SampFreq = 20;
t = 1/SampFreq:1/SampFreq:length(Sig)/SampFreq;

wavename='cmor3-3';
totalscal=1024; %尺度序列的长度，即scal的长度
wcf=centfrq(wavename); %小波的中心频率
cparam=2*wcf*totalscal; %为得到合适的尺度所求出的参数
a=totalscal:-1:1;
scal=cparam./a; %得到各个尺度，以使转换得到频率序列为等差序列
coefs=cwt(Sig,scal,wavename); %得到小波系数
f1=scal2frq(scal,wavename,1/Fs1); %将尺度转换为频率

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% figure %%二维图
% imagesc(t,f1,abs(coefs)); %绘制色谱图
% set(gca, 'YDir', 'normal')
% colorbar;
% xlabel('时间 t/s');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5


% window = 256;
% Nfrebin = 1024;
%
% [Spec,f1] = STFT(Sig',SampFreq,Nfrebin,window);
% picdata=abs(Spec);

picdata=abs(coefs);
[xIn yIn]=localMaximum(picdata,[10,80]);
%locs=find(f1<1);
% thrs=0.1*max(max(picdata(1:locs(end),:))); %%在[0,1]Hz搜索极值
thrs=0.2*10^(-4);
[Ix,Iy]=find(picdata>=thrs);
m=length(xIn);
locx=[];locy=[];
for jj=1:m
    if ismember(xIn(jj),Ix)&&ismember(yIn(jj),Iy)
        locx=[locx;xIn(jj)];
        locy=[locy;yIn(jj)];
    end
end
% figure;hold on; %%三维图
% mesh(t,f1,picdata);
% plot3(t(locy),f1(locx),picdata(locx,locy),'rp','markersize',10);
% xlabel('Time (s)');
% ylabel('Frequency (Hz)');
% title('coefs');

% frqs1=unique(f1(locx))
frqs1=f1(locx);
% addrs1=find(frqs1>1&frqs1<1.75) %%限制频带[0.1,0.7]Hz
% if length(addrs1)>0
%     result=unique(frqs1(addrs1))
%     if length(result)>1
%         count=hist(frqs1(addrs1),result)
%         [vals,inds]=max(count);           %%出现频次最大的频率作为呼吸率
%         br_s2=result(inds)
%     else br_s2=result
%     end
%     amps=max(max(picdata(locx(addrs1),locy(addrs1))));
%     [indx,indy]=find(picdata(locx,locy)==amps); %%幅度（能量）最大的频率作为呼吸率
%     br_s1=frqs1(indx(1))
% else
%     br_s2=0
%     br_s1=0
% end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
addrs1=find(frqs1>1&frqs1<1.75); %%限制频带[0.8,2]Hz
if length(addrs1)>0
    result=unique(frqs1(addrs1));
    result*60
    if length(result)>1
        count=hist(frqs1(addrs1),result)
        [vals,inds]=max(count);           %%出现频次最大的频率作为心率
        hr_s2=result(inds);
    else hr_s2=result
    end
    amps=max(max(picdata(locx(addrs1),locy(addrs1))));
    [indx,indy]=find(picdata(locx,locy)==amps); %%幅度（能量）最大的频率作为心率
    hr_s1=frqs1(indx(1));
else
    hr_s2=0;
    hr_s1=0;
end
hr_s2=round(hr_s2*60)
hr_s1=round(hr_s1*60)
% hr_s1=round(hr_s1*60);
% br_s1=round(br_s1*60);
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%