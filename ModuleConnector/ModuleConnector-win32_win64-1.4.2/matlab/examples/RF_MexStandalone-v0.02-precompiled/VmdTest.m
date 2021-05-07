function [bre1, bre2, bre3, bre4, bre5]=VmdTest(RawData)

peopleOfExist   = [1,0,0,1,0];   %五个位置 1 代表有人 0 代表没人

K = 2;
rangeOfLocation = [79,156,261,271,296;
    157,233,338,349,374;];

%0319
% rangeOfLocation = [87,156,273,279,307;
%                   164,233,350,356,384;];  %T 296-374   0328

testRawData=RawData;

measuredRespiration=zeros(1,5);

Batches=size(RawData,1);
SpeedOfLight=3*10^8;
Resolution=0.00386751476861213;

Fs=SpeedOfLight/(Resolution*2);
[bandfilter]=qfir(Fs);
FrameStitchnum=size(RawData,2)/256;
BandpassData=zeros(Batches,256*FrameStitchnum);
ClutterData=zeros(Batches,256*FrameStitchnum);
PureData=zeros(Batches,256*FrameStitchnum);
aanum=zeros(200,1);


pnum=256;
firnum=50;
alpha=0.5;
kesai=0.50;


for raw=1:1:Batches
    for framenum=1:FrameStitchnum
        blockdata=RawData(raw,(framenum-1)*pnum+1:framenum*pnum);
        blockmean=mean(blockdata);
        DCmean=repmat(blockmean,1,pnum);
        RawData(raw,(framenum-1)*pnum+1:framenum*pnum)=blockdata-DCmean;                  %去直流
        
    end
    convres=conv(RawData(raw,:),bandfilter);
    BandpassData(raw,:)=convres(1,firnum/2+1:firnum/2+256*FrameStitchnum);
end

%PCA去杂波
s = svd(BandpassData);
[U,S,V] = svd(BandpassData);


%PCA去掉第一个主元矩阵
Data = BandpassData - U(:,:)*S(:,1:1)*V(:,1:1)';
testData = Data;



for Location = 1:5
    
    start =  rangeOfLocation(1,Location);
    eend  =  rangeOfLocation(2,Location);
    
    for iLocation=start:eend
        energyOfLocation(iLocation,Location) = sum(Data(:,iLocation).*Data(:,iLocation));
    end
    
    
    dou = energyOfLocation(:,Location);          %取出 某个位置 所在范围内所有快时间列的能量
    
    [energymax(1),energymaxi(1)] = max(dou);
    
    %     dou(energymaxi(1))=0;
    %     [energymax(2),energymaxi(2)] = max(dou);
    %
    %     dou(energymaxi(2))=0;
    %     [energymax(3),energymaxi(3)] = max(dou);
    %
    %     dou(energymaxi(3))=0;
    %     [energymax(4),energymaxi(4)] = max(dou);
    %
    %     dou(energymaxi(4))=0;
    %     [energymax(5),energymaxi(5)] = max(dou);           %enerymaxi（） 中存储了前五大能量的快时间值
    
    %     for i=1:4
    %         dou(energymaxi(i))=0;
    %         [energymax(i+1),energymaxi(i+1)] = max(dou);
    %
    %     end                                                      %enerymaxi（） 中存储了前五大能量的快时间值
    
    
    DData = Data(:,energymaxi(1));                  %取出认为是生命信号的一列
    
    % some sample parameters for VMD
    alpha = 2000; % moderate bandwidth constraint
    tau = 0;      % noise-tolerance (no strict fidelity enforcement)噪声耐受，一般取0就行
    %K = 2;        % 3 modes
    DC = 0;       % no DC part imposed
    init = 1;     % initialize omegas uniformly
    tol = 1e-7;   %总信号拟合误差允许程度
    
    %--------------- Run actual VMD code
    
    [u, u_hat, omega] = VMD(DData, alpha, tau, K, DC, init, tol);                          %VMD中 只有DData这个位置需要做变化
    
    %--------------- Visualization
    
    % For convenience here: Order omegas increasingly and reindex u/u_hat
    [~, sortIndex] = sort(omega(end,:));
    omega = omega(:,sortIndex);
    u_hat = u_hat(:,sortIndex);
    u = u(sortIndex,:);        %u中存了K个VMD分解量
    
    
    for i =1:K
        fre(i,:)=abs(fftshift(fft(u(i,:),2^16)))*1000;
    end
    
    frequencyk2(:,Location) = fre(2,:);
    frequencyk1(:,Location) = fre(1,:);
    
    Y = [(-2^16/2:2^16/2-1)*(40)/2^16];
    %plot(Y,frequencyk2(:,Location));
    [resultvalue,result] = max(fre(1,:));
    measuredRespirationK1(Location) = abs(Y(result));
    
    [resultvalue,result] = max(fre(2,:));
    measuredRespirationK2(Location) = abs(Y(result));
    
    measuredRespiration(Location) = measuredRespirationK1(Location);
    
    if measuredRespiration(Location)<0.03
        measuredRespiration(Location) = measuredRespirationK2(Location);
    end
    
    if (Location>=2)&&(sum(peopleOfExist)>1)
        measuredRespiration(Location) = measuredRespirationK2(Location);
    end
    
    if measuredRespiration(Location)>3
        measuredRespiration(Location) = measuredRespirationK1(Location);
    end
    
    
end

bre1 = measuredRespiration(1);
bre2 = measuredRespiration(2);
bre3 = measuredRespiration(3);
bre4 = measuredRespiration(4);
bre5 = measuredRespiration(5);

% 
% realRespiration
% measuredRespiration







