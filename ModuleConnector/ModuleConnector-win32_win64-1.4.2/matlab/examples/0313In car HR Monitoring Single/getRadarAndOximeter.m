%%%%%%%%%实时读取雷达与血氧仪心跳，并画图111111111111111111111111111111111%%%%%%%%%%%%%%%%%%%%%%%%%%
clear
clc
close

format long g   %时间不是指数形式

hbradar1 = 0;

hbxueyangyi1=0;

radartime = 0;
radarbox1=zeros(1,6);        %存储画图用的十个点

xueyangyibox1=zeros(1,6);    %存储血氧仪画图用的十个点

timebox = zeros(1,6);

lalala1 = zeros(1,3);

countplot1=0;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%雷达读数据%%%%%%%%%%%%%%%%%%%%%%
addpath('../../../matlab/');
addpath('../../../include/');
addpath('../../../lib64/');
addpath('../');
Lib = ModuleConnector.Library;
% Input parameters
COM = 'COM4';
FPS = 20;
dataType = 'rf';

% Chip settings
PPS = 26;
DACmin = 949;
DACmax = 1100;
Iterations = 16;
FrameStart = 0.2; % meters.
FrameStop = 3; % meters.

filecount = 0;

% Create BasicRadarClassX4 object
radar = BasicRadarClassX4(COM,FPS,dataType);

% Open radar.
radar.open();

% Use X4M300 interface to attempt to set sensor mode XEP (manual).
app = radar.mc.get_x4m300();

app.set_sensor_mode('stop');
try
    app.set_sensor_mode('XEP');
catch
    % Unable to set sensor mode. Assume only running XEP FW.
end

% Initialize radar.
radar.init();

% Configure X4 chip.
radar.radarInstance.x4driver_set_pulsesperstep(PPS);
radar.radarInstance.x4driver_set_dac_min(DACmin);
radar.radarInstance.x4driver_set_dac_max(DACmax);
radar.radarInstance.x4driver_set_iterations(Iterations);

% Configure frame area
radar.radarInstance.x4driver_set_frame_area(FrameStart,FrameStop);
% Read back actual set frame area
[frameStart, frameStop] = radar.radarInstance.x4driver_get_frame_area();

% Start streaming and subscribe to message_data_float.
radar.start();

i=1;
c=0;
RawData=[];

while (1)
    
    % Peek message data float
    numPackets = radar.bufferSize();
    
    if numPackets> 0;
        % Get frame (uses read_message_data_float)
        [frame, ctr] = radar.GetFrameNormalized();
        RawData=[RawData;frame'];
        
        
        %s=datestr(now,'yyyymmddHHMMSSFFF');
        s=datestr(now,'HHMMSS.FFF');    %%%%%%%%%%%%%%%%%得到读取这一帧的时间
        
        timestamp(i)=str2num(s);
        timestamp = timestamp';
        i=i+1;
    end
    if mod(i,301)==0
       c=c+1;
        RawData=[timestamp RawData];    
        RawData(:,1)=[];

         heart = demo(RawData);
 
   
%         heart = demo(RawData);
        
        hbradar1=heart(1)
    
      
        radartime = timestamp(200);
        radartime=mod(radartime,10000);
%         
        timetime = floor(mod(timestamp(200),1000000));
%         
%         
%         [xueyangyihb1,xueyangyitime1] = oximeter1();    %得到血氧仪心率值或者-1
%        % [xueyangyihb2,xueyangyitime2] = oximeter2();    %得到血氧仪心率值或者-1
%       %  [xueyangyihb3,xueyangyitime3] = oximeter3();    %得到血氧仪心率值或者-1
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
%         if(xueyangyihb1~=-1)
%             hbxueyangyi1=xueyangyihb1(size(xueyangyitime1,2));
%             for jjj=1:1:size(xueyangyitime1,2)
%                 if abs(xueyangyitime1(jjj)-radartime)<1
%                     hbxueyangyi1 = xueyangyihb1(jjj);
%                     answer = 'duiqi';
%                     break
%                 end
%             end
%         else
%             hbxueyangyi1 = -1;
%         end
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%       
%         if(xueyangyihb2~=-1)
%             hbxueyangyi2=xueyangyihb2(size(xueyangyitime2,2));
%             for jjj=1:1:size(xueyangyitime2,2)
%                 if abs(xueyangyitime2(jjj)-radartime)<1
%                     hbxueyangyi2 = xueyangyihb2(jjj);
%                     answer = 'duiqi';
%                     break
%                 end
%             end
%         else
%             hbxueyangyi2 = -1;
%         end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
%          if(xueyangyihb3~=-1)
%             hbxueyangyi3=xueyangyihb3(size(xueyangyitime3,2));
%             for jjj=1:1:size(xueyangyitime3,2)
%                 if abs(xueyangyitime3(jjj)-radartime)<1
%                     hbxueyangyi3 = xueyangyihb3(jjj);
%                     answer = 'duiqi';
%                     break
%                 end
%             end
%         else
%             hbxueyangyi3 = -1;
%         end       
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
         
       
%         lll=sum(sum(PureData.*PureData,2))  ;            %利用阈值判断是否有人，无人置零
%          
%         if lll<0.01
%             
%             hbradar1=0;
%             hbradar2=0;
%             hbradar3=0;
%             
%         end
        
         
         
%         figure(1)
       
        %%%%%%%%%画图1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%画图1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        subplot(2,1,1);
        
        
        lalala1(3) = [];
        lalala1=[hbradar1 lalala1];
        
        countplot1=countplot1+1;                  %求平均
        
        if countplot1 >3
            if hbradar1==0
                hbradar1 = 0;
            else
                hbradar1 = mean(lalala1);
            end
        else
            hbradar1 = 0;
        end
        
        
        radarbox1(6) = [];
        radarbox1=[hbradar1 radarbox1];
        radarbox1=floor(radarbox1);
        
%         xueyangyibox1(6) = [];
%         xueyangyibox1 = [hbxueyangyi1 xueyangyibox1];
%         
%         timebox(6) = [];
%         timebox = [timetime,timebox];
%         
        radarbox1(1) = [];
        radarbox1=[radarbox1 hbradar1];    %存
        radarbox1=floor(radarbox1);
        
        xueyangyibox1(1) = [];
        xueyangyibox1 = [xueyangyibox1 hbxueyangyi1];
        
        timebox(1) = [];
        timebox = [timebox timetime];
        
        if hbradar1>100
            plot(1:6,radarbox1,'k');%黑色异常雷达
        elseif hbradar1==0
            plot(1:6,radarbox1,'g');%绿色无人雷达
        else 
            plot(1:6,radarbox1,'r');%红色正常雷达
        end
        xlim([1,6]);
        ylim([40,140]);

        for i = 1:length(radarbox1)
            if radarbox1(i) ~=0
                text(i-0.1,radarbox1(i)+1,{[num2str(radarbox1(i))]},'FontSize',13,'FontWeight','bold','color','red');%写数字
            end
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%% legend
        ll=legend('雷达','血氧仪');
        qqq=get(ll,'Position');
        set( ll,'Position',[qqq(1)-0.65,qqq(2),qqq(3),qqq(4)]);
        set(ll,'FontWeight','bold','FontSize',16);
            
        set(gca,'XTickLabel','')                                      
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        xlabel('时间');
        ylabel('心率 次数/分钟');
        
        for jj = 1:6         
            textstr=sprintf('%02d:%02d:%02d',floor(timebox(jj)/10000),floor(mod(timebox(jj),10000)/100),mod(timebox(jj),100));
            text(jj -0.12 ,35,{textstr},'FontSize',9,'FontWeight','bold','color','black');
        end 
        
        pause(0.01)      
        


        RawData = [];
        timestamp=[];
        i=1;
        
    end
end

