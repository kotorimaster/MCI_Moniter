function [people input_my]=realtime_countingtry_nor(RawData,xiu)
tic
FrameStitchnum=5;
SpeedOfLight=3*10^8;
Resolution=1/256;
Fs=SpeedOfLight/(Resolution*2);
[bandfilter]=qfir(Fs);
%Receive Raw Data
Batches=50;
pnum=256;
firnum=100;
people=0;
Iteration=10;

for raw=1:1:Batches
 for framenum=1:FrameStitchnum
     blockdata=RawData(raw,(framenum-1)*pnum+1:framenum*pnum);
     blockmean=mean(blockdata);
     DCmean=repmat(blockmean,1,pnum);
     RawData(raw,(framenum-1)*pnum+1:framenum*pnum)=blockdata-DCmean; 
 end
 convres=conv(RawData(raw,:),bandfilter);
 BandpassData(raw,:)=convres(1,firnum/2+1:firnum/2+256*FrameStitchnum); 
end
%%%%%%%%%%%%%%%%%%%%%%%%%%去噪%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sigma=1;
PureData_denoise=zeros(Batches,256*FrameStitchnum);
C1 = fdct_wrapping(BandpassData,1,2);
E = cell(size(C1));
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
PureData_denoise=ifdct_wrapping(Qt,1);
noise =BandpassData - PureData_denoise;
%%%%%%%%%%%%%%%%%%%%%%%%%%去噪%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
varia = [];
for my_batch = 1:Batches
    input_my =[];
meanmean=mean(BandpassData(my_batch,:));           %第一个特征
variance=var(BandpassData(my_batch,:));        %第二个特征   

m = 1;
num_channel = 1;
ts = 10/(3*256);

Td1=0.5;
Td2=1;
Td3=1.5;
Td4=2;
Td5=2.5;
Td6=3;
Td7=3.5;

Tobs=16.64;
BandpassData0 = BandpassData(my_batch,1:Tobs/ts);

PureData_denoise1 = PureData_denoise(my_batch,1:Tobs/ts);
PureData_denoise2 = PureData_denoise1;
PureData_denoise3 = PureData_denoise1;
PureData_denoise4 = PureData_denoise1;
PureData_denoise5 = PureData_denoise1;
PureData_denoise6 = PureData_denoise1;
PureData_denoise7 = PureData_denoise1;

varn=var(noise(my_batch,:));

Nsb1=fix(Td1/ts);
Nsb2=fix(Td2/ts);
Nsb3=fix(Td3/ts);
Nsb4=fix(Td4/ts);
Nsb5=fix(Td5/ts);
Nsb6=fix(Td6/ts);
Nsb7=fix(Td7/ts);

number_of_bin1=fix(Tobs/Td1);
number_of_bin2=fix(Tobs/Td2);
number_of_bin3=fix(Tobs/Td3);
number_of_bin4=fix(Tobs/Td4);
number_of_bin5=fix(Tobs/Td5);
number_of_bin6=fix(Tobs/Td6);
number_of_bin7=fix(Tobs/Td7);

Ebin1 = zeros(num_channel,number_of_bin1);
Ebin2 = zeros(num_channel,number_of_bin2);
Ebin3 = zeros(num_channel,number_of_bin3);
Ebin4 = zeros(num_channel,number_of_bin4);
Ebin5 = zeros(num_channel,number_of_bin5);
Ebin6 = zeros(num_channel,number_of_bin6);
Ebin7 = zeros(num_channel,number_of_bin7);

Abin1 = zeros(num_channel,number_of_bin1);
Abin2 = zeros(num_channel,number_of_bin2);
Abin3 = zeros(num_channel,number_of_bin3);
Abin4 = zeros(num_channel,number_of_bin4);
Abin5 = zeros(num_channel,number_of_bin5);
Abin6 = zeros(num_channel,number_of_bin6);
Abin7 = zeros(num_channel,number_of_bin7);

[m,n]=size(BandpassData0);
Erb=BandpassData0.^2;


for j1 = 1:number_of_bin1
    Na1=0;
    for k1=1:Nsb1
        Ebin1(1,j1) = Ebin1(1,j1)+Erb(1,(j1-1)*Nsb1+k1);
        Abin1(1,j1) = Abin1(1,j1)+abs(PureData_denoise1(1,(j1-1)*Nsb1+k1));
        if abs(PureData_denoise1(1,(j1-1)*Nsb1+k1)) > 1e-4
            Na1=Na1+1;
        end
    end;
    if Na1~=0
        Abin1(1,j1)=Abin1(1,j1)/Na1;
    end
end
Abin_square1=Abin1.^2;
fk1 = Ebin1/varn;
Es1=zeros(1,number_of_bin1);
for i1 = 1:number_of_bin1
    Es1(1,i1) =Abin_square1(1,i1);
end


for j2 = 1:number_of_bin2
    Na2=0;
    for k2=1:Nsb2
        Ebin2(1,j2) = Ebin2(1,j2)+Erb(1,(j2-1)*Nsb2+k2);
        Abin2(1,j2) = Abin2(1,j2)+abs(PureData_denoise2(1,(j2-1)*Nsb2+k2));
        if abs(PureData_denoise2(1,(j2-1)*Nsb2+k2)) > 1e-4
            Na2=Na2+1;
        end
    end;
    if Na2~=0
        Abin2(1,j2)=Abin2(1,j2)/Na2;
    end
end
Abin_square2=Abin2.^2;
fk2 = Ebin2/varn;
Es2=zeros(1,number_of_bin2);
for i2 = 1:number_of_bin2
    Es2(1,i2) =Abin_square2(1,i2);
end

for j3 = 1:number_of_bin3
    Na3=0;
    for k3=1:Nsb3
        Ebin3(1,j3) = Ebin3(1,j3)+Erb(1,(j3-1)*Nsb3+k3);
        Abin3(1,j3) = Abin3(1,j3)+abs(PureData_denoise3(1,(j3-1)*Nsb3+k3));
        if abs(PureData_denoise3(1,(j3-1)*Nsb3+k3)) > 1e-4
            Na3=Na3+1;
        end
    end;
    if Na3~=0
        Abin3(1,j3)=Abin3(1,j3)/Na3;
    end
end
Abin_square3=Abin3.^2;
fk3 = Ebin3/varn;
Es3=zeros(1,number_of_bin3);
for i3 = 1:number_of_bin3
    Es3(1,i3) =Abin_square3(1,i3);
end

for j4 = 1:number_of_bin4
    Na4=0;
    for k4=1:Nsb4
        Ebin4(1,j4) = Ebin4(1,j4)+Erb(1,(j4-1)*Nsb4+k4);
        Abin4(1,j4) = Abin4(1,j4)+abs(PureData_denoise4(1,(j4-1)*Nsb4+k4));
        if abs(PureData_denoise4(1,(j4-1)*Nsb4+k4)) > 1e-4
            Na4=Na4+1;
        end
    end;
    if Na4~=0
        Abin4(1,j4)=Abin4(1,j4)/Na4;
    end
end
Abin_square4=Abin4.^2;
fk4 = Ebin4/varn;
Es4=zeros(1,number_of_bin4);
for i4 = 1:number_of_bin4
    Es4(1,i4) =Abin_square4(1,i4);
end

for j5 = 1:number_of_bin5
    Na5=0;
    for k5=1:Nsb5
        Ebin5(1,j5) = Ebin5(1,j5)+Erb(1,(j5-1)*Nsb5+k5);
        Abin5(1,j5) = Abin5(1,j5)+abs(PureData_denoise5(1,(j5-1)*Nsb5+k5));
        if abs(PureData_denoise5(1,(j5-1)*Nsb5+k5)) > 1e-4
            Na5=Na5+1;
        end
    end;
    if Na5~=0
        Abin5(1,j5)=Abin5(1,j5)/Na5;
    end
end
Abin_square5=Abin5.^2;
fk5 = Ebin5/varn;
Es5=zeros(1,number_of_bin5);
for i5 = 1:number_of_bin5
    Es5(1,i5) =Abin_square5(1,i5);
end

for j6 = 1:number_of_bin6
    Na6=0;
    for k6=1:Nsb6
        Ebin6(1,j6) = Ebin6(1,j6)+Erb(1,(j6-1)*Nsb6+k6);
        Abin6(1,j6) = Abin6(1,j6)+abs(PureData_denoise6(1,(j6-1)*Nsb6+k6));
        if abs(PureData_denoise6(1,(j6-1)*Nsb6+k6)) > 1e-4
            Na6=Na6+1;
        end
    end;
    if Na6~=0
        Abin6(1,j6)=Abin6(1,j6)/Na6;
    end
end
Abin_square6=Abin6.^2;
fk6 = Ebin6/varn;
Es6=zeros(1,number_of_bin6);
for i6 = 1:number_of_bin6
    Es6(1,i6) =Abin_square6(1,i6);
end

for j7 = 1:number_of_bin7
    Na7=0;
    for k7=1:Nsb7
        Ebin7(1,j7) = Ebin7(1,j7)+Erb(1,(j7-1)*Nsb7+k7);
        Abin7(1,j7) = Abin7(1,j7)+abs(PureData_denoise7(1,(j7-1)*Nsb7+k7));
        if abs(PureData_denoise7(1,(j7-1)*Nsb7+k7)) > 1e-4
            Na7=Na7+1;
        end
    end;
    if Na7~=0
        Abin7(1,j7)=Abin7(1,j7)/Na7;
    end
end
Abin_square7=Abin7.^2;
fk7 = Ebin7/varn;
Es7=zeros(1,number_of_bin7);
for i7 = 1:number_of_bin7
    Es7(1,i7) =Abin_square7(1,i7);
end

fk1 = mapminmax(fk1,0,1);
Es1 = mapminmax(Es1,0,1);

fk2 = mapminmax(fk2,0,1);
Es2 = mapminmax(Es2,0,1);

fk3 = mapminmax(fk3,0,1);
Es3 = mapminmax(Es3,0,1);

fk4 = mapminmax(fk4,0,1);
Es4 = mapminmax(Es4,0,1);

fk5 = mapminmax(fk5,0,1);
Es5 = mapminmax(Es5,0,1);

fk6 = mapminmax(fk6,0,1);
Es6 = mapminmax(Es6,0,1);

fk7 = mapminmax(fk7,0,1);
Es7 = mapminmax(Es7,0,1);


input_my=[meanmean variance fk1 Es1 fk2 Es2 fk3 Es3 fk4 Es4 fk5 Es5 fk6 Es6 fk7 Es7];
people1 = classRF_predict_xiu(input_my,xiu);
varia = [varia people1]

end
 people = fix(median(varia));


toc