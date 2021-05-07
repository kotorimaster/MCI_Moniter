function [pp, PureData7]=che_countxiu(RawData7,xiu)
tic
FrameStitchnum=3;
SpeedOfLight=3*10^8;
Resolution=1/256;
Fs=SpeedOfLight/(Resolution*2);
[bandfilter]=qfir(Fs);
%Receive Raw Data
Batches=200;
pnum=256;
firnum=100;
people=0;
Ebin1mean = [];
Abin1mean = [];
Emax1mean = [];
Emax_denoise1mean = [];
Ebin2mean = [];
Abin2mean = [];
Emax2mean = [];
Emax_denoise2mean = [];
Ebin3mean = [];
Abin3mean = [];
Emax3mean = [];
Emax_denoise3mean = [];
alpha = 0.5;

for raw=1:1:Batches
 for framenum=1:FrameStitchnum
     blockdata7=RawData7(raw,(framenum-1)*pnum+1:framenum*pnum);
     blockmean7=mean(blockdata7);
     DCmean7=repmat(blockmean7,1,pnum);
     RawData7(raw,(framenum-1)*pnum+1:framenum*pnum)=blockdata7-DCmean7; 
 end 
 convres7=conv(RawData7(raw,:),bandfilter);
 BandpassData7(raw,:)=convres7(1,firnum/2+1:firnum/2+256*FrameStitchnum);
 if raw==1
     ClutterData7(raw,:)=(1-alpha)*BandpassData7(raw,:);
 end
 if raw>1
     ClutterData7(raw,:)=alpha*ClutterData7(raw-1,:)+(1-alpha)*BandpassData7(raw,:);
 end
end
PureData7=BandpassData7-ClutterData7;

C1 = fdct_wrapping(PureData7,1,2);
E = cell(size(C1));
sigma=1;
 for s=1:length(C1)
   E{s} = cell(size(C1{s}));
   for w=1:length(C1{s})
     A = C1{s}{w};
     E{s}{w} = median(abs(A(:) - median(A(:))))/.6745; 
   end
 end
Ct=C1;
Qt=C1;
 %对每个子带的变换系数做硬阈值处理
for s = 2:length(C1)
  thresh = 3*sigma + sigma*(s == length(C1));
  
%在阈值的选取上,是保留较大的系数,舍弃较小的系数, 因为根据Curvelet变换理论, 较大的Curvelet系数对应于较强的边缘,反之为噪声
  for w = 1:length(C1{s})
    Qt{s}{w} = C1{s}{w}.* (abs(C1{s}{w}) > thresh*E{s}{w});
  end
end

PureData7_denoise=ifdct_wrapping(Qt,1);

PureData7 = PureData7(11:end,:);
BandpassData7 = BandpassData7(11:end,:);
PureData7_denoise = PureData7_denoise(11:end,:);
variable_mean = [];   
for my_batch = 1:(Batches-10)
% my_batch = 100;

    m = 1;
    num_channel = 1;
    ts = 10/(3*256);

PureData = PureData7(my_batch,:);
PureData_denoise = PureData7_denoise(my_batch,:);

Nsb1 = 16;
Nsb2 = 32;
Nsb3 = 64;

number_of_bin1 = 48;
number_of_bin2 = 24;
number_of_bin3 = 12;

Ebin1 = zeros(num_channel,number_of_bin1);
Abin1 = zeros(num_channel,number_of_bin1);
Emax1 = zeros(num_channel,number_of_bin1);
Emax_denoise1 = zeros(num_channel,number_of_bin1);

Ebin2 = zeros(num_channel,number_of_bin2);
Abin2 = zeros(num_channel,number_of_bin2);
Emax2 = zeros(num_channel,number_of_bin2);
Emax_denoise2 = zeros(num_channel,number_of_bin2);

Ebin3 = zeros(num_channel,number_of_bin3);
Abin3 = zeros(num_channel,number_of_bin3);
Emax3 = zeros(num_channel,number_of_bin3);
Emax_denoise3 = zeros(num_channel,number_of_bin3);

[m,n]=size(PureData);
Erb = PureData.^2;
Ers = PureData_denoise.^2;

for j1 = 1:number_of_bin1
    for k1=1:Nsb1
        Ebin1(1,j1) = Ebin1(1,j1)+Erb(1,(j1-1)*Nsb1+k1);
        Abin1(1,j1) = Abin1(1,j1)+Ers(1,(j1-1)*Nsb1+k1);
    end;
    Emax1(1,j1) = max(PureData(1,(j1-1)*Nsb1+1:j1*Nsb1));
    Emax_denoise1(1,j1) = max(PureData_denoise(1,(j1-1)*Nsb1+1:j1*Nsb1));
end
for j2 = 1:number_of_bin2
    for k2=1:Nsb2
        Ebin2(1,j2) = Ebin2(1,j2)+Erb(1,(j2-1)*Nsb2+k2);
        Abin2(1,j2) = Abin2(1,j2)+Ers(1,(j2-1)*Nsb2+k2);
    end;
    Emax2(1,j2) = max(PureData(1,(j2-1)*Nsb2+1:j2*Nsb2));
    Emax_denoise2(1,j2) = max(PureData_denoise(1,(j2-1)*Nsb2+1:j2*Nsb2));
end
for j3 = 1:number_of_bin3
    for k3=1:Nsb3
        Ebin3(1,j3) = Ebin3(1,j3)+Erb(1,(j3-1)*Nsb3+k3);
        Abin3(1,j3) = Abin3(1,j3)+Ers(1,(j3-1)*Nsb3+k3);
    end;
    Emax3(1,j3) = max(PureData(1,(j3-1)*Nsb3+1:j3*Nsb3));
    Emax_denoise3(1,j3) = max(PureData_denoise(1,(j3-1)*Nsb3+1:j3*Nsb3));
end
Ebin1mean = [Ebin1mean; Ebin1];
Abin1mean = [Abin1mean; Abin1];
Emax1mean = [Emax1mean; Emax1];
Emax_denoise1mean = [Emax_denoise1mean; Emax_denoise1];
Ebin2mean = [Ebin2mean; Ebin2];
Abin2mean = [Abin2mean; Abin2];
Emax2mean = [Emax2mean; Emax2];
Emax_denoise2mean = [Emax_denoise2mean; Emax_denoise2];
Ebin3mean = [Ebin3mean; Ebin3];
Abin3mean = [Abin3mean; Abin3];
Emax3mean = [Emax3mean; Emax3];
Emax_denoise3mean = [Emax_denoise3mean; Emax_denoise3];
end
Ebin1meanmean = mean(Ebin1mean);
Abin1meanmean = mean(Abin1mean);
Emax1meanmean = mean(Emax1mean);
Emax_denoise1meanmean = mean(Emax_denoise1mean);
Ebin2meanmean = mean(Ebin2mean);
Abin2meanmean = mean(Abin2mean);
Emax2meanmean = mean(Emax2mean);
Emax_denoise2meanmean = mean(Emax_denoise2mean);
Ebin3meanmean = mean(Ebin3mean);
Abin3meanmean = mean(Abin3mean);
Emax3meanmean = mean(Emax3mean);
Emax_denoise3meanmean = mean(Emax_denoise3mean);
input_my = [Ebin1meanmean Abin1meanmean Emax1meanmean Emax_denoise1meanmean Ebin2meanmean Abin2meanmean Emax2meanmean Emax_denoise2meanmean Ebin3meanmean Abin3meanmean Emax3meanmean Emax_denoise3meanmean]; 
people = classRF_predict_xiu(input_my,xiu);
% varia = [varia people1]
if people == 0
    pp = [0 0 0 0 0];
elseif people == 1
    pp = [1 0 0 0 0];
elseif people == 2
    pp = [0 1 0 0 0];
elseif people == 3
    pp = [0 0 1 0 0];
elseif people == 4
    pp = [0 0 0 1 0];
elseif people == 5
    pp = [0 0 0 0 1];
elseif people == 6
    pp = [1 1 0 0 0];
elseif people == 7
    pp = [1 0 1 0 0];
elseif people == 8
    pp = [1 0 0 1 0];
elseif people == 9
    pp = [1 0 0 0 1];
elseif people == 10
    pp = [1 1 1 0 0];
elseif people == 11
    pp = [1 1 0 1 0];
elseif people == 12
    pp = [1 1 0 0 1];
elseif people == 13
    pp = [1 0 1 1 0];
elseif people == 14
    pp = [1 0 1 0 1];
elseif people == 15
    pp = [1 0 0 1 1];
end
%  people = mode(varia)


% toc