function [pp]=che_xiuxiuxiu426(RawData7,xiu)
tic
FrameStitchnum=3;
SpeedOfLight=3*10^8;
Resolution=1/256;
Fs=SpeedOfLight/(Resolution*2);
[bandfilter]=qfir(Fs);
%Receive Raw Data
Batches=200;
pnum=256;
firnum=50;
people=0;
% Ebin1mean = [];
% Abin1mean = [];
% Emax1mean = [];
% Emax_denoise1mean = [];
% Ebin2mean = [];
% Abin2mean = [];
% Emax2mean = [];
% Emax_denoise2mean = [];
% Ebin3mean = [];
% Abin3mean = [];
% Emax3mean = [];
% Emax_denoise3mean = [];
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
PureData=BandpassData7-ClutterData7;

PureData = PureData(11:end,:);
C = fdct_wrapping(PureData,1,2);
St1=cell(size(C));

for s=1:length(C)
    for w=1:length(C{s})
        St1{s}{w}=zeros(size(C{s}{w}));
    end
end

% St1{1} = C{1};
St1{2}{6} = C{2}{6};
St1{2}{7} = C{2}{7};
St1{2}{14} = C{2}{14};
St1{2}{15} = C{2}{15};
St1{3}{12} = C{3}{12};
St1{3}{13} = C{3}{13};
St1{3}{28} = C{3}{28};
St1{3}{29} = C{3}{29};
St1{4}{12} = C{4}{12};
St1{4}{13} = C{4}{13};
St1{4}{28} = C{4}{28};
St1{4}{29} = C{4}{29};
% St1{5} = C{5};

PureData777=ifdct_wrapping(St1,1,190,768);
% PureData7 = mapminmax(PureData7(:,1:500));

C1 = fdct_wrapping(PureData777,1,2);
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

PureData7 = mapminmax(PureData777(:,1:500));
% BandpassData7 = mapminmax(BandpassData7(:,1:500));
PureData7_denoise = mapminmax(PureData7_denoise(:,1:500));
variable_meanmean = [];

C = fdct_wrapping(PureData777(:,1:500),1,2);

St_co = C{1};
Coarse_energy = sum(sum(St_co{1}.^2));   %Coarse层能量
Corse_mean = mean(mean(St_co{1}));       %Coarse层均值

St_fi = C{5};
Fine_energy = sum(sum(St_fi{1}.^2));     %Fine层能量
an = sort(St_fi{1},1,'descend');
ann = sort(an,2,'descend');
Fine_max = ann(1,1:5);                   %Fine层最大值

detail1 = sum(sum(C{2}{6}.^2))+sum(sum(C{2}{7}.^2))+sum(sum(C{2}{14}.^2))+sum(sum(C{2}{15}.^2)); 
detail2 = sum(sum(C{3}{12}.^2))+sum(sum(C{3}{13}.^2))+sum(sum(C{3}{28}.^2))+sum(sum(C{3}{29}.^2));   
detail3 = sum(sum(C{4}{12}.^2))+sum(sum(C{4}{13}.^2))+sum(sum(C{4}{28}.^2))+sum(sum(C{4}{29}.^2));

PureDataxiao7 = abs(PureData7);
PureData_e=sum(PureDataxiao7.^2,1)./Batches;

number_of_bin1 = 50;
number_of_bin2 = 25;

Ebin1 = zeros(Batches-10,number_of_bin1);
Abin1 = zeros(Batches-10,number_of_bin1);
Emax1 = zeros(Batches-10,number_of_bin1);
Emax_denoise1 = zeros(Batches-10,number_of_bin1);

Ebin2 = zeros(Batches-10,number_of_bin2);
Abin2 = zeros(Batches-10,number_of_bin2);
Emax2 = zeros(Batches-10,number_of_bin2);
Emax_denoise2 = zeros(Batches-10,number_of_bin2);


for my_batch = 1:(Batches-10)
    m = 1;
    num_channel = 1;
    ts = 10/(3*256);

PureData = PureData7(my_batch,:);
PureData_denoise = PureData7_denoise(my_batch,:);

Nsb1 = 10;
Nsb2 = 20;

[m,n]=size(PureData);
Erb = PureData.^2;
Ers = PureData_denoise.^2;

for j1 = 1:number_of_bin1
    for k1=1:Nsb1
        Ebin1(my_batch,j1) = Ebin1(my_batch,j1)+Erb(1,(j1-1)*Nsb1+k1);
        Abin1(my_batch,j1) = Abin1(my_batch,j1)+Ers(1,(j1-1)*Nsb1+k1);
    end;
    Emax1(my_batch,j1) = max(PureData(1,(j1-1)*Nsb1+1:j1*Nsb1));
    Emax_denoise1(my_batch,j1) = max(PureData_denoise(1,(j1-1)*Nsb1+1:j1*Nsb1));
end
for j2 = 1:number_of_bin2
    for k2=1:Nsb2
        Ebin2(my_batch,j2) = Ebin2(my_batch,j2)+Erb(1,(j2-1)*Nsb2+k2);
        Abin2(my_batch,j2) = Abin2(my_batch,j2)+Ers(1,(j2-1)*Nsb2+k2);
    end;
    Emax2(my_batch,j2) = max(PureData(1,(j2-1)*Nsb2+1:j2*Nsb2));
    Emax_denoise2(my_batch,j2) = max(PureData_denoise(1,(j2-1)*Nsb2+1:j2*Nsb2));
end

energy(my_batch,1)=sum(PureData_e);
e_front(my_batch,1)=sum(PureData_e(:,1:200));
e_back(my_batch,1)=sum(PureData_e(:,205:400));
e1(my_batch,1)=sum(PureData_e(:,1:55));
e2(my_batch,1)=sum(PureData_e(:,56:130));
e3(my_batch,1)=sum(PureData_e(:,245:263));
e4(my_batch,1)=sum(PureData_e(:,220:244));
e5(my_batch,1)=sum(PureData_e(:,264:300));
%最大值
[ampmax(my_batch,1),maxloc(my_batch,1)]=max(max(PureDataxiao7,[],1));
[ampmax1(my_batch,1),maxloc1(my_batch,1)]=max(PureData_e(:,1:55));
[ampmax2(my_batch,1),maxloc2(my_batch,1)]=max(PureData_e(:,56:130));
[ampmax3(my_batch,1),maxloc3(my_batch,1)]=max(PureData_e(:,245:263));
[ampmax4(my_batch,1),maxloc4(my_batch,1)]=max(PureData_e(:,220:244));
[ampmax5(my_batch,1),maxloc5(my_batch,1)]=max(PureData_e(:,264:300));
%幅值
amp=mean(PureDataxiao7,1);
ampmean(my_batch,1)=mean(amp);
am_front(my_batch,1)=mean(amp(1,1:200));
am_back(my_batch,1)=mean(amp(1,205:400));
end
variable = [energy e_front e_back e1 e2 e3 e4 e5 ampmax ampmax1 ampmax2 ampmax3 ampmax4 ampmax5 ampmean am_front am_back Ebin1 Abin1 Emax1 Emax_denoise1 Ebin2 Abin2 Emax2 Emax_denoise2];
variable_mean = mean(variable);
input_my = [Coarse_energy Corse_mean Fine_energy Fine_max detail1 detail2 detail3 variable_mean];

% input_my = [energymean e_frontmean e_backmean e1mean e2mean e3mean e4mean e5mean ampmaxmean ampmax1mean ampmax2mean ampmax3mean ampmax4mean ampmax5mean ampmeanmean am_frontmean am_backmean]; 
people = classRF_predict_xiu(input_my,xiu);
% varia = [varia people1]
if people == 0
    pp = [0 0 0 0 0];
elseif people == 1
    pp = [1 0 0 0 0];
elseif people == 2
    pp = [1 1 0 0 0];
elseif people == 3
    pp = [1 0 1 0 0];
elseif people == 4
    pp = [1 0 0 1 0];
elseif people == 5
    pp = [1 0 0 0 1];
elseif people == 6
    pp = [1 1 1 0 0];
elseif people == 7
    pp = [1 1 0 1 0];
elseif people == 8
    pp = [1 1 0 0 1];
elseif people == 9
    pp = [1 0 1 1 0];
elseif people == 10
    pp = [1 0 1 0 1];
elseif people == 11
    pp = [1 0 0 1 1];
end
%  people = mode(varia)


% toc