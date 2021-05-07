%%%%%%%%%实时读取雷达与血氧仪心跳，并画图2222222222222222222222222222222222222222222222222222222222%%%%%%%%%%%%%%%%%%%%%%%%%%
clear
clc
close

format long g   %时间不是指数形式

hbradar1 = 0;
hbradar2 = 0;
hbradar3 = 0;
xueyangyihb1=0;
xueyangyihb2=0;
hbxueyangyi3=0;
radartime = 0;
radarbox1=zeros(1,6);        %存储画图用的十个点
radarbox2=zeros(1,6);        %存储画图用的十个点
radarbox3=zeros(1,6);        %存储画图用的十个点
xueyangyibox1=zeros(1,6);    %存储血氧仪画图用的十个点
xueyangyibox2=zeros(1,6);    %存储血氧仪画图用的十个点
xueyangyibox3=zeros(1,6);    %存储血氧仪画图用的十个点
lalala1 = zeros(1,3); 
lalala2 = zeros(1,3);
lalala3 = zeros(1,3);
countplot1=0;
countplot2=0;
countplot3=0;

timebox = zeros(1,6);

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
        i=i+1
    end
    if mod(i,301)==0
       
        RawData=[timestamp RawData];    
        RawData(:,1)=[];
        

        heart = demo(RawData);
        
        hbradar1=heart(1);
        hbradar2=heart(2);
       % hbradar3=heart(3);
      
        radartime = timestamp(200);
        radartime=mod(radartime,10000);
        timetime = floor(mod(timestamp(200),1000000));
        [xueyangyitime1,xueyangyihb1,xueyangyitime2,xueyangyihb2]=oxi_yandiansai();
%         [xueyangyihb1,xueyangyitime1] = oximeter1();    %得到血氧仪心率值或者-1
%         [xueyangyihb2,xueyangyitime2] = oximeter2();    %得到血氧仪心率值或者-1
      %  [xueyangyihb3,xueyangyitime3] = oximeter3();    %得到血氧仪心率值或者-1
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
%         if(xueyangyihb1~=-1)
%             xueyangyihb1=xueyangyihb1(size(xueyangyitime1,2));
%             for jjj=1:1:size(xueyangyitime1,2)
%                 if abs(xueyangyitime1(jjj)-radartime)<1
%                     xueyangyihb1 = xueyangyihb1(jjj);
%                     answer = 'duiqi';
%                     break
%                 end
%             end
%         else
%             xueyangyihb1 = -1;
%         end
%  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%       
%         if(xueyangyihb2~=-1)
%             xueyangyihb2=xueyangyihb2(size(xueyangyitime2,2));
%             for jjj=1:1:size(xueyangyitime2,2)
%                 if abs(xueyangyitime2(jjj)-radartime)<1
%                     xueyangyihb2 = xueyangyihb2(jjj);
%                     answer = 'duiqi';
%                     break
%                 end
%             end
%         else
%             xueyangyihb2 = -1;
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
         
        PureData = newfilter(RawData);
%         lll=sum(sum(PureData.*PureData,2))  ;            %利用阈值判断是否有人，无人置零
%          
%         if lll<0.01
%             
%             hbradar1=0;
%             hbradar2=0;
%             hbradar3=0;
%             
%         end
        
         
         
        figure(1)
        %%%%%%%%%画图1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%画图1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        subplot(2,1,1);
        
        
        lalala1(3) = [];
        lalala1=[hbradar1 lalala1];
        
        countplot1=countplot1+1;
        
        if countplot1 >3
            if hbradar1==0
                hbradar1 = 0;
            else
                hbradar1 = mean(lalala1);
            end
        else
            hbradar1 = 0;
        end
        
        radarbox1(1) = [];
        radarbox1=[radarbox1 hbradar1];
        radarbox1=floor(radarbox1);
        
        xueyangyibox1(1) = [];
        xueyangyibox1 = [xueyangyibox1 xueyangyihb1]
        
        timebox(1) = [];
        timebox = [timebox timetime];      
        
        
        plot(1:6,radarbox1,'r');
        title('Driver');
        xlim([1,6]);
        ylim([40,140]);

        for i = 1:length(radarbox1)
            if radarbox1(i) ~=0 
                text(i-0.1,radarbox1(i)+1,{[num2str(radarbox1(i))]},'FontSize',13,'FontWeight','bold','color','red');
            end
        end
        
        hold on
        plot(1:6,xueyangyibox1,'b');
        title('Driver');
        xlim([1,6]);
        ylim([40,140]);
        for i = 1:length(xueyangyibox1)
            if xueyangyibox1(i)~=0
                text(i-0.1,xueyangyibox1(i)+1,{[num2str(xueyangyibox1(i))]},'FontSize',13,'FontWeight','bold','color','blue');
       
            end
        end       
        text(5.9,radarbox1(6)-11,{'\uparrow'},'FontSize',13,'FontWeight','bold','color','red');
        text(5.6,radarbox1(6)-16,{'New Data'},'FontSize',13,'FontWeight','bold','color','red');
        
        
        
        hold off
        
        ll=legend('Radar','Oximeter');
%         qqq=get(ll,'Position');
%         set( ll,'Position',[qqq(1)-0.65,qqq(2),qqq(3),qqq(4)]);
%         set(ll,'FontWeight','bold','FontSize',16);
        
        
        
        set(gca,'XTickLabel','')

     

        xlabel('Time');
        ylabel('Heart Rate/Beat Per Minute');
        
         for jj = 1:6         
            textstr=sprintf('%02d:%02d:%02d',floor(timebox(jj)/10000),floor(mod(timebox(jj),10000)/100),mod(timebox(jj),100));
            text(jj -0.12 ,35,{textstr},'FontSize',9,'FontWeight','bold','color','black');
        end
        
        
        pause(0.01)      
        %%%%%%%%%画图1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%画图1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        
        
         %%%%%%%%%画图2%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%画图2%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        subplot(2,1,2);
        
        
        lalala2(3) = [];
        lalala2=[hbradar2 lalala2];
        
        countplot2=countplot2+1;
        
        if countplot2 >3
            if hbradar2==0
                hbradar2 = 0;
            else
                hbradar2 = mean(lalala2);
            end
        else
            hbradar2 = 0;
        end
        
        radarbox2(1) = [];
        radarbox2=[radarbox2 hbradar2];
        radarbox2=floor(radarbox2);
        
        xueyangyibox2(1) = [];
        xueyangyibox2 = [xueyangyibox2 xueyangyihb2]
radarbox2=[0,0,0,0,0,0]
xueyangyibox2=[0,0,0,0,0,0]
        plot(radarbox2,'r');
        title('Passenger（Location 2）');
        xlim([1,6]);
        ylim([40,140]);

        for i = 1:length(radarbox2)
            if radarbox2(i) ~=0
                text(i-0.1,radarbox2(i)+1,{[num2str(radarbox2(i))]},'FontSize',13,'FontWeight','bold','color','red');
            end
        end
        
        hold on
        plot(1:6,xueyangyibox2,'b');
        xlim([1,6]);
        ylim([40,140]);
        for i = 1:length(xueyangyibox2)
            if xueyangyibox2(i) ~=0
             text(i-0.1,xueyangyibox2(i)+1,{[num2str(xueyangyibox2(i))]},'FontSize',13,'FontWeight','bold','color','blue');
            end
        end 
        text(5.9,radarbox2(6)-11,{'\uparrow'},'FontSize',13,'FontWeight','bold','color','red');
        text(5.6,radarbox2(6)-16,{'New Data'},'FontSize',13,'FontWeight','bold','color','red');
     
        hold off
        
        ll=legend('Radar','Oximeter');
%         qqq=get(ll,'Position');
%         set( ll,'Position',[qqq(1)-0.65,qqq(2),qqq(3),qqq(4)]);
%         set(ll,'FontWeight','bold','FontSize',16);
        
        
        set(gca,'XTickLabel','')
        
        xlabel('Time');
        ylabel('Heart Rate/Beat Per Minute');
        
        for jj = 1:6         
            textstr=sprintf('%02d:%02d:%02d',floor(timebox(jj)/10000),floor(mod(timebox(jj),10000)/100),mod(timebox(jj),100));
            text(jj -0.12 ,35,{textstr},'FontSize',9,'FontWeight','bold','color','black');
        end 
        
        pause(0.01)      
        %%%%%%%%%画图2%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%画图2%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%       
        
        
        
        %%%%%%%%%画图3%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%画图3%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%         
%         subplot(3,1,3);
%         
%         
%         lalala3(3) = [];
%         lalala3=[hbradar3 lalala3];
%         
%         countplot3=countplot3+1;
%         
%         if countplot3 >3
%             if hbradar3==0
%                 hbradar3 = 0;
%             else
%                 hbradar3 = mean(lalala3);
%             end
%         end
%         
%         radarbox3(10) = [];
%         radarbox3=[hbradar3 radarbox3];
%         radarbox3=floor(radarbox3);
%         
%         xueyangyibox3(10) = [];
%         xueyangyibox3 = [hbxueyangyi3 xueyangyibox3];
%         
%         plot(radarbox3,'r');
%         xlim([1,10]);
%         ylim([40,120]);
% 
%         for i = 1:length(radarbox3)
%             text(i,radarbox3(i)+1,{[num2str(radarbox3(i))]},'FontSize',8,'FontWeight','bold','color','red');
%         end
%         
%         hold on
%         plot(xueyangyibox3,'b');
%         xlim([1,10]);
%         ylim([40,120]);
%         for i = 1:length(xueyangyibox3)
%             text(i,xueyangyibox3(i)+1,{[num2str(xueyangyibox3(i))]},'FontSize',8,'FontWeight','bold','color','blue');
%         end        
%         hold off
%         legend('Radar','Oximeter');
%         pause(0.01)      
        %%%%%%%%%画图3%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%画图3%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
        
   
        RawData = [];
        timestamp=[];
        i=1;
        
    end
end

