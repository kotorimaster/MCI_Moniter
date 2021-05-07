clear
clc
close

addpath('../../../matlab/');
addpath('../../../include/');
addpath('../../../lib64/');
addpath('../');
Lib = ModuleConnector.Library;
% Input parameters
COM = 'COM9';
FPS = 20;
dataType = 'rf';

% Chip settings
PPS = 26;
DACmin = 949;
DACmax = 1100;
Iterations = 16;
FrameStart = 0.2; % meters.
FrameStop = 3; % meters.

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

i = 0;
M=0;L=0;K=1;
pg=1;rx_num=2;
br_s=0;hr_s=0;
smoothp=zeros(5,1);
smoothp1=zeros(5,1);
global flag1
flag1=1;
i=1;
RawData=[];
flag=0;
while (1)
    % Peek message data float
    numPackets = radar.bufferSize();
    
    if numPackets> 0;
        % Get frame (uses read_message_data_float)
        [frame, ctr] = radar.GetFrameNormalized();
        RawData=[RawData;frame'];
        
        s=datestr(now,31);
        s(5)=[];s(7)=[];s(9)=[];s(11)=[];s(13)=[];
        timestamp(i)=str2num(s);
        timestamp = timestamp';
        
        
        
        i=i+1;
    end
    if mod(i,21)==0
        
        
        p='C:\Users\mac\Desktop\À×´ïÊý¾Ý625\';
        
        s=datestr(now,31);
        s(17)='-';s(14)='-';s(11)='-';
        path=strcat(p,s);
        RawData=[timestamp RawData];
        dlmwrite(path,RawData,'precision','%5f','delimiter','\t')
        
 
       flag=1;
        
    end

    if(flag==1)
        break;
    end
end

% Stop streaming.
radar.stop();
% Output short summary report.
framesRead = i;
totFramesFromChip = ctr;

% FPS_est = framesRead/tspent;

framesDropped = ctr-i;
radar.close();
clear radar frame