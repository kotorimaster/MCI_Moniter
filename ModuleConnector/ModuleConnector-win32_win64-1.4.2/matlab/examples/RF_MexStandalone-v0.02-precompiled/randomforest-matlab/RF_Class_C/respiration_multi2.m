%% time delay by cross correlation
%%�拎?���@���������ʁA?��?�g�A?�g
% RawData=load('C:\Users\Wenfeng\Desktop\RawData\static\2016-07-08-20-46-53.txt');
function [br_s2,hr_s2]=respiration_multi2(Pure)
% RawData=load('F:\ProData\cl\static\1\radar\2016-07-15-21-39-28.txt');

T=size(Pure,1);
peaks=zeros(1,T);tops=zeros(1,T);
for pp=1:size(Pure,1)
    [vv,tmp]=max(abs(Pure(pp,:)));
    peaks(pp)=tmp;  %% position
    tops(pp)=vv;  %% amplitude
end

L1=50;
peaks=medfilt1(peaks,L1);

adz=log(tops);
sm=max(tops);
tm=peaks(find(tops==sm));
adz=adz-max(adz); %% ln(Sm)-ln(Sa);
dm=max(peaks);
dx=min(peaks);
t0=[];
fxx=[];
ai=zeros(length(adz),1);bi=zeros(length(adz),1);ci=zeros(length(adz),1);
for i=1:length(adz)
    if adz(i)~=0
       ai(i)=1;
       bi(i)=9*(peaks(i)-tm)/adz(i)-2*dm;
       ci(i)=dm^2+(9/2)*(peaks(i)^2-tm^2)/adz(i); 
    else
        ai(i)=1;bi(i)=-2*dm;ci(i)=dm^2;
    end
end
delta=sqrt(bi.^2-4*ai.*ci);
fxx=[-bi-delta,-bi+delta];
fxx=real(fxx);

for i=1:length(adz)
    if abs(fxx(i,1))<=abs(fxx(i,2))
        t0(i)=fxx(i,1);
    else t0(i)=fxx(i,2);
    end
end
adz=peaks+t0;

Sig=adz;
Fs1=40;
w1=0.1/(Fs1/2);w2=1.8/(Fs1/2);
[a,b]=butter(5,[w1 w2],'bandpass');
Sig=filter(a,b,Sig);
SampFreq = 40;

wavename='cmor3-3';
totalscal=1024; %�߶����еĳ��ȣ���scal�ĳ���
wcf=centfrq(wavename); %С��������Ƶ��
cparam=2*wcf*totalscal; %Ϊ�õ����ʵĳ߶�������Ĳ���
a=totalscal:-1:1; 
scal=cparam./a; %�õ������߶ȣ���ʹת���õ�Ƶ������Ϊ�Ȳ�����
coefs=cwt(Sig,scal,wavename); %�õ�С��ϵ��
f1=scal2frq(scal,wavename,1/Fs1); %���߶�ת��ΪƵ��
% figure; %%��άͼ
% imagesc(t,f1,abs(coefs)); %����ɫ��ͼ
% set(gca, 'YDir', 'normal')
% colorbar;
% xlabel('ʱ�� t/s');

picdata=abs(coefs);
[xIn yIn]=localMaximum(picdata,[10,80]);
locs=find(f1<1);
thrs=0.25*max(max(picdata(1:locs(end),:))); %%��[0,1]Hz������ֵ
[Ix,Iy]=find(picdata>=thrs);
m=length(xIn);
locx=[];locy=[];
for jj=1:m
    if ismember(xIn(jj),Ix)&&ismember(yIn(jj),Iy)
        locx=[locx;xIn(jj)];
        locy=[locy;yIn(jj)];
    end
end
% figure;hold on; %%��άͼ
% mesh(t,f1,picdata); 
% plot3(t(locy),f1(locx),picdata(locx,locy),'rp','markersize',10);
% xlabel('Time (s)');
% ylabel('Frequency (Hz)');
% title('coefs');

% frqs1=unique(f1(locx))
frqs1=f1(locx)
addrs1=find(frqs1>0.1&frqs1<1); %%����Ƶ��[0.1,0.7]Hz
if length(addrs1)>0
result=unique(frqs1(addrs1))    
if length(result)>1
count=hist(frqs1(addrs1),result)
[vals,inds]=max(count);           %%����Ƶ������Ƶ����Ϊ������
br_s2=result(inds)     
else br_s2=result
end
amps=max(max(picdata(locx(addrs1),locy(addrs1))));
[indx,indy]=find(picdata(locx,locy)==amps); %%���ȣ�����������Ƶ����Ϊ������
br_s1=frqs1(indx(1))
else
    br_s2=0
    br_s1=0
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
addrs1=find(frqs1>1&frqs1<2); %%����Ƶ��[0.8,2]Hz
if length(addrs1)>0
result=unique(frqs1(addrs1))    
if length(result)>1
count=hist(frqs1(addrs1),result)
[vals,inds]=max(count);           %%����Ƶ������Ƶ����Ϊ����
hr_s2=result(inds)     
else hr_s2=result
end
amps=max(max(picdata(locx(addrs1),locy(addrs1))));
[indx,indy]=find(picdata(locx,locy)==amps); %%���ȣ�����������Ƶ����Ϊ����
hr_s1=frqs1(indx(1))
else
    hr_s2=1.33;
    hr_s1=1.33;
end
hr_s2=round(hr_s2*60);
br_s2=round(br_s2*60);
end
