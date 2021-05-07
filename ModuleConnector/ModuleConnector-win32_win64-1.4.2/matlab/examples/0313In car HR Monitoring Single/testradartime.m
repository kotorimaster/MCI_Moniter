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
COM = 'COM5';
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
        i=i+1;
    end
    if mod(i,301)==0
       
        RawData=[timestamp RawData];    
        RawData(:,1)=[];
        heart=heartbeat2(RawData);
        
        tic
        pause(5)
        toc
      
        radartime = timestamp(200);
        radartime=floor(mod(radartime,10000))
        

        RawData = [];
        timestamp=[];
        i=1;
        
    end
end

