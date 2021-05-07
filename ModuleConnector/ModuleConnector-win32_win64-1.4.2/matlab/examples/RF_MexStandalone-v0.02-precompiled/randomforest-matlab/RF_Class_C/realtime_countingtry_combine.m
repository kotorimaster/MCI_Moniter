function [people input_my]=realtime_countingtry_combine(RawData,xiu)
tic
FrameStitchnum=5;
SpeedOfLight=3*10^8;
Resolution=1/256;
Fs=SpeedOfLight/(Resolution*2);
[bandfilter]=qfir(Fs);
%Receive Raw Data
Batches=200;
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
C = fdct_wrapping(BandpassData,1,2);
St1=cell(size(C));
St2=cell(size(C));
St3=cell(size(C));

St4=cell(size(C));
St5=cell(size(C));
St6=cell(size(C));

St7=cell(size(C));
St8=cell(size(C));
for s=1:length(C)
    for w=1:length(C{s})
        St1{s}{w}=zeros(size(C{s}{w}));
        St2{s}{w}=zeros(size(C{s}{w}));
        St3{s}{w}=zeros(size(C{s}{w}));
        
        St4{s}{w}=zeros(size(C{s}{w}));
        St5{s}{w}=zeros(size(C{s}{w}));
        St6{s}{w}=zeros(size(C{s}{w}));
        
        St7{s}{w}=zeros(size(C{s}{w}));
        St8{s}{w}=zeros(size(C{s}{w}));
    end
end

St1{2}{2} = C{2}{2};
St1{2}{3} = C{2}{3};
St1{2}{10} = C{2}{10};
St1{2}{11} = C{2}{11};

St2{3}{4} = C{3}{4};
St2{3}{5} = C{3}{5};
St2{3}{20} = C{3}{20};
St2{3}{21} = C{3}{21};

St3{4}{4} = C{4}{4};
St3{4}{5} = C{4}{5};
St3{4}{20} = C{4}{20};
St3{4}{21} = C{4}{21};

St4{2}{6} = C{2}{6};
St4{2}{7} = C{2}{7};
St4{2}{14} = C{2}{14};
St4{2}{15} = C{2}{15};

St5{3}{12} = C{3}{12};
St5{3}{13} = C{3}{13};
St5{3}{28} = C{3}{28};
St5{3}{29} = C{3}{29};

St6{4}{12} = C{4}{12};
St6{4}{13} = C{4}{13};
St6{4}{28} = C{4}{28};
St6{4}{29} = C{4}{29};

St7{1} = C{1};

St8{5} = C{5};

PureData1=ifdct_wrapping(St1,1,200,1280);
PureData2=ifdct_wrapping(St2,1,200,1280);
PureData3=ifdct_wrapping(St3,1,200,1280);

ClutterData1=ifdct_wrapping(St4,1,200,1280);
ClutterData2=ifdct_wrapping(St5,1,200,1280);
ClutterData3=ifdct_wrapping(St6,1,200,1280);

Coarst1 = ifdct_wrapping(St7,1,200,1280);
Finest1 = ifdct_wrapping(St8,1,200,1280);

varia = [];
for my_batch = 1:Batches
input_my =[];
my_batch = 100;
meanmean=mean(BandpassData(my_batch,:));           %第一个特征
variance=var(BandpassData(my_batch,:));        %第二个特征   

mean1 = mean(PureData1(my_batch,:));
mean11 = mean(PureData1(my_batch,:).^2);
mean111 = mean(PureData1(my_batch,:).^3);
var1 = var(PureData1(my_batch,:));
energy1 = sum(abs(PureData1(my_batch,:)).^2);

mean2 = mean(PureData2(my_batch,:));
mean22 = mean(PureData2(my_batch,:).^2);
mean222 = mean(PureData2(my_batch,:).^3);
var2 = var(PureData2(my_batch,:));
energy2 = sum(abs(PureData2(my_batch,:)).^2);

mean3 = mean(PureData3(my_batch,:));
mean33 = mean(PureData3(my_batch,:).^2);
mean333 = mean(PureData3(my_batch,:).^3);
var3 = var(PureData3(my_batch,:));
energy3 = sum(abs(PureData3(my_batch,:)).^2);

mean4 = mean(ClutterData1(my_batch,:));
mean44 = mean(ClutterData1(my_batch,:).^2);
mean444 = mean(ClutterData1(my_batch,:).^3);
var4 = var(ClutterData1(my_batch,:));
energy4 = sum(abs(ClutterData1(my_batch,:)).^2);

mean5 = mean(ClutterData2(my_batch,:));
mean55 = mean(ClutterData2(my_batch,:).^2);
mean555 = mean(ClutterData2(my_batch,:).^3);
var5 = var(ClutterData2(my_batch,:));
energy5 = sum(abs(ClutterData2(my_batch,:)).^2);

mean6 = mean(ClutterData3(my_batch,:));
mean66 = mean(ClutterData3(my_batch,:).^2);
mean666 = mean(ClutterData3(my_batch,:).^3);
var6 = var(ClutterData3(my_batch,:));
energy6 = sum(abs(ClutterData3(my_batch,:)).^2);

mean7 = mean(Coarst1(my_batch,:));
mean77 = mean(Coarst1(my_batch,:).^2);
mean777 = mean(Coarst1(my_batch,:).^3);
var7 = var(Coarst1(my_batch,:));
energy7 = sum(abs(Coarst1(my_batch,:)).^2);

mean8 = mean(Finest1(my_batch,:));
mean88 = mean(Finest1(my_batch,:).^2);
mean888 = mean(Finest1(my_batch,:).^3);
var8 = var(Finest1(my_batch,:));
energy8 = sum(abs(Finest1(my_batch,:)).^2);

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



input_my=[meanmean variance fk1 Es1 fk2 Es2 fk3 Es3 fk4 Es4 fk5 Es5 fk6 Es6 fk7 Es7 mean1 mean11 mean111 var1 energy1 mean2 mean22 mean222 var2 energy2 mean3 mean33 mean333 var3 energy3 mean4 mean44 mean444 var4 energy4 mean5 mean55 mean555 var5 energy5 mean6 mean66 mean666 var6 energy6 mean7 mean77 mean777 var7 energy7 mean8 mean88 mean888 var8 energy8];
people1 = classRF_predict_xiu(input_my,xiu);
varia = [varia people1]

end
 people = median(varia)


toc