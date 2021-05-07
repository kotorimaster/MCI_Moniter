function [people input_my]=realtime_countingtry_CT(RawData,xiu)
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
% meanmean=mean(BandpassData(my_batch,:));           %第一个特征
% variance=var(BandpassData(my_batch,:));        %第二个特征   

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




input_my=[mean1 mean11 mean111 var1 energy1 mean2 mean22 mean222 var2 energy2 mean3 mean33 mean333 var3 energy3 mean4 mean44 mean444 var4 energy4 mean5 mean55 mean555 var5 energy5 mean6 mean66 mean666 var6 energy6 mean7 mean77 mean777 var7 energy7 mean8 mean88 mean888 var8 energy8];
people1 = classRF_predict_xiu(input_my,xiu);
varia = [varia people1]

end
 people = median(varia)


toc