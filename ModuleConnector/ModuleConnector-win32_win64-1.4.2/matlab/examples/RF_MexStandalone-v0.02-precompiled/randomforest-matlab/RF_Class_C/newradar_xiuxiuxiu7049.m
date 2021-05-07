function [pp]=newradar_xiuxiuxiu7049(RawData7,xiu)
M=0;L=0;K=1;
pg=1;rx_num=2;
Batches = 200;
people=0;
PureData=pca_filter_x4x(RawData7,rx_num,pg,M,L,K);

PureData = PureData(11:end,:);
for ii = 1:Batches
    DPureData(ii,:) = PureData(ii,1:437);
    DgPureData(ii,:) = mapminmax(DPureData(ii,:),-1,1);
end

DgrPureData = DgPureData(10:end,:);
PureData777 = DgrPureData;

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
 %��ÿ���Ӵ��ı任ϵ����Ӳ��ֵ����
for s = 2:length(C1)
  thresh = 3*sigma + sigma*(s == length(C1));
  
%����ֵ��ѡȡ��,�Ǳ����ϴ��ϵ��,������С��ϵ��, ��Ϊ����Curvelet�任����, �ϴ��Curveletϵ����Ӧ�ڽ�ǿ�ı�Ե,��֮Ϊ����
  for w = 1:length(C1{s})
    Qt{s}{w} = C1{s}{w}.* (abs(C1{s}{w}) > thresh*E{s}{w});
  end
end

PureData7_denoise=ifdct_wrapping(Qt,1);

PureData7 = mapminmax(PureData777(:,1:400));
% BandpassData7 = mapminmax(BandpassData7(:,1:500));
PureData7_denoise = mapminmax(PureData7_denoise(:,1:400));
variable_meanmean = [];

C = fdct_wrapping(PureData777(:,1:400),1,2);

St_co = C{1};
Coarse_energy = sum(sum(St_co{1}.^2));   %Coarse������
Corse_mean = mean(mean(St_co{1}));       %Coarse���ֵ

St_fi = C{5};
Fine_energy = sum(sum(St_fi{1}.^2));     %Fine������
an = sort(St_fi{1},1,'descend');
ann = sort(an,2,'descend');
Fine_max = ann(1,1:5);                   %Fine�����ֵ

detail1 = sum(sum(C{2}{6}.^2))+sum(sum(C{2}{7}.^2))+sum(sum(C{2}{14}.^2))+sum(sum(C{2}{15}.^2)); 
detail2 = sum(sum(C{3}{12}.^2))+sum(sum(C{3}{13}.^2))+sum(sum(C{3}{28}.^2))+sum(sum(C{3}{29}.^2));   
detail3 = sum(sum(C{4}{12}.^2))+sum(sum(C{4}{13}.^2))+sum(sum(C{4}{28}.^2))+sum(sum(C{4}{29}.^2));

PureDataxiao7 = abs(PureData7);
% PureData_e=sum(PureDataxiao7.^2,1)./Batches;

number_of_bin1 = 50;
number_of_bin2 = 25;
number_of_bin3 = 5;

Ebin1 = zeros(Batches-10,number_of_bin1);
Abin1 = zeros(Batches-10,number_of_bin1);
Emax1 = zeros(Batches-10,number_of_bin1);
Emax_denoise1 = zeros(Batches-10,number_of_bin1);

Ebin2 = zeros(Batches-10,number_of_bin2);
Abin2 = zeros(Batches-10,number_of_bin2);
Emax2 = zeros(Batches-10,number_of_bin2);
Emax_denoise2 = zeros(Batches-10,number_of_bin2);

Ebin3 = zeros(Batches-10,number_of_bin3);
Abin3 = zeros(Batches-10,number_of_bin3);
Emax3 = zeros(Batches-10,number_of_bin3);
Emax_denoise3 = zeros(Batches-10,number_of_bin3);

for my_batch = 1:(Batches-10)
    m = 1;
    num_channel = 1;
    ts = 10/(3*256);

% PureData_e(my_batch,:)=sum(PureDataxiao7(my_batch,:).^2,1);
PureData_e(my_batch,:)=PureDataxiao7(my_batch,:).^2;
PureData = PureData7(my_batch,:);
PureData_denoise = PureData7_denoise(my_batch,:);

Nsb1 = 8;
Nsb2 = 16;
Nsb3 = 80;

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
for j3 = 1:number_of_bin3
    for k3=1:Nsb3
        Ebin3(my_batch,j3) = Ebin3(my_batch,j3)+Erb(1,(j3-1)*Nsb3+k3);
        Abin3(my_batch,j3) = Abin3(my_batch,j3)+Ers(1,(j3-1)*Nsb3+k3);
    end;
    Emax3(my_batch,j3) = max(PureData(1,(j3-1)*Nsb3+1:j3*Nsb3));
    Emax_denoise3(my_batch,j3) = max(PureData_denoise(1,(j3-1)*Nsb3+1:j3*Nsb3));
end

energy(my_batch,1)=sum(PureData_e(my_batch,:));
e_front(my_batch,1)=sum(PureData_e(my_batch,1:125));
e_back(my_batch,1)=sum(PureData_e(my_batch,126:227));
e1(my_batch,1)=sum(PureData_e(my_batch,1:86));
e2(my_batch,1)=sum(PureData_e(my_batch,87:125));
e3(my_batch,1)=sum(PureData_e(my_batch,126:212));
e4(my_batch,1)=sum(PureData_e(my_batch,150:212));
e5(my_batch,1)=sum(PureData_e(my_batch,180:300));
%���ֵ
[ampmax(my_batch,1),maxloc(my_batch,1)]=max(max(PureDataxiao7(my_batch,:),[],1));
[ampmax1(my_batch,1),maxloc1(my_batch,1)]=max(PureData_e(my_batch,1:86));
[ampmax2(my_batch,1),maxloc2(my_batch,1)]=max(PureData_e(my_batch,87:125));
[ampmax3(my_batch,1),maxloc3(my_batch,1)]=max(PureData_e(my_batch,126:212));
[ampmax4(my_batch,1),maxloc4(my_batch,1)]=max(PureData_e(my_batch,150:212));
[ampmax5(my_batch,1),maxloc5(my_batch,1)]=max(PureData_e(my_batch,180:300));
%��ֵ
amp=mean(PureDataxiao7(my_batch,:),1);
ampmean(my_batch,1)=mean(amp);
am_front(my_batch,1)=mean(amp(1,1:125));
am_back(my_batch,1)=mean(amp(1,126:227));
end
variable = [energy e_front e_back e1 e2 e3 e4 e5 ampmax ampmax1 ampmax2 ampmax3 ampmax4 ampmax5 ampmean am_front am_back Ebin1 Abin1 Emax1 Emax_denoise1 Ebin2 Abin2 Emax2 Emax_denoise2 Ebin3 Abin3 Emax3 Emax_denoise3];
variable_mean = mean(variable);
variable_meanmean = [Coarse_energy Corse_mean Fine_energy Fine_max detail1 detail2 detail3 variable_mean];

% input_my = [energymean e_frontmean e_backmean e1mean e2mean e3mean e4mean e5mean ampmaxmean ampmax1mean ampmax2mean ampmax3mean ampmax4mean ampmax5mean ampmeanmean am_frontmean am_backmean]; 
people = classRF_predict_xiu(variable_meanmean,xiu);
% varia = [varia people1]
if people == 0
    pp = [0 0 0 0 0];
elseif people == 1
    pp = [1 0 0 0 0];
elseif people == 2
    pp = [1 1 0 0 0];
elseif people == 3
    pp = [1 1 1 0 0];
elseif people == 4
    pp = [1 1 0 1 0];
elseif people == 5
    pp = [1 1 0 0 1];
    elseif people == 6
    pp = [1 0 1 1 0];
elseif people == 7
    pp = [1 0 1 0 1];
elseif people == 8
    pp = [1 0 0 1 1];
end
%  people = mode(varia)


% toc