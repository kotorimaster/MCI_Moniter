%% time delay by cross correlation
%%愭嫀?墑岪嫀捈棳暘検丄?捠?攇丄?攇
function [br_v,hr_v]=respiration_multi2_vncmd(Pure)
% function [br_v,hr_v,br_s,hr_s]=respiration_multi2_vncmd(Pure)

T=size(Pure,1);
peaks=zeros(1,T);tops=zeros(1,T);
for pp=1:size(Pure,1)
    [vv,tmp]=max(abs(Pure(pp,:)));
    peaks(pp)=tmp;  %% position
    tops(pp)=vv;  %% amplitude
end

L1=50;
% peaks=medfilt1(peaks,L1); %%中值滤波
peaks=kalmanfilter_3(peaks,Pure);

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
%     if abs(fxx(i,1))<=abs(fxx(i,2))
    if peaks(i)>=tm||fxx(i,1)>tm
        t0(i)=fxx(i,1);
    else
        t0(i)=2*tm-fxx(i,1);
    end
end
adz=peaks'+t0;

Sig=adz;
Fs1=40;
w1=0.1/(Fs1/2);w2=2/(Fs1/2);
[a,b]=butter(5,[w1 w2],'bandpass');
Sig=filter(a,b,Sig);
SampFreq = 40;
t = 1/SampFreq:1/SampFreq:length(Sig)/SampFreq;
%% STFT
window = 256;
Nfrebin = 1024;

[Spec,f] = STFT(Sig',SampFreq,Nfrebin,window);

%% ridge extraction and smoothing
% bw = SampFreq/80;% the bandwidth of the TF filter for ridge extraction
bw = SampFreq/40;
beta1 = 1e-4; % beta1 should be larger than the following beta
num = 4; % the number of the components
M=2;
delta = 10;
[fidexmult, tfdv] = extridge_mult(Sig, SampFreq, num, delta, beta1,bw,Nfrebin,window);

%% parameter setting
alpha = 1e-5; 
beta = 1e-5; % this parameter can be smaller which will be helpful for the convergence, but it may cannot properly track fast varying IFs
iniIF = curvesmooth(f(fidexmult),beta); % the initial guess for the IFs by ridge detection; the initial IFs should be smooth and thus we smooth the detected ridges
% var = maxvalue;% noise variance
var = 1;
tol = 1e-3;%

[IFmset IA smset sdif] = VNCMD2_2(Sig,SampFreq,iniIF,alpha,beta,var,tol);

frqs_v=mean(IFmset(:,:,end),2);
hr_v=fix(frqs_v(2)*60);
br_v=fix(frqs_v(1)*60);
wh=smset(2,:,end)./IA(1,:);
bt=smset(1,:,end)./IA(2,:);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% frqs=mean(iniIF(:,:),2)             %%%% STFT 初始化频率，未优化
% loc1=find(frqs>1&frqs<2);
% [val1,addrs1]=min(abs(frqs(loc1)-hr_v));
% hr_s=frqs(loc1(addrs1))
% loc2=find(frqs>0.01&frqs<0.5);
% [val2,addrs2]=min(abs(frqs(loc2)-br_v));
% br_s=frqs(loc2(addrs2))
end
