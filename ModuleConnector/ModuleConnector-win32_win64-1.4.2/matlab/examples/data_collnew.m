addpath('../../../matlab/');
addpath('../../../include/');
addpath('../../../lib64/');
addpath('../');
Lib = ModuleConnector.Library;
% Input parameters
COM = 'COM8';
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

i=1;
RawData=[];
% while (1)
fornum= 1;

% for tiaoshu=1:fornum
%     for hangshu = 1:200
        % Peek message data float
        numPackets = radar.bufferSize(); 
        if numPackets> 0;
            % Get frame (uses read_message_data_float)
            [frame, ctr] = radar.GetFrameNormalized();
            RawData=[RawData;frame']
        end
%     end
% p='C:\Users\mac\Desktop\新雷达数据\0\';
% s=datestr(now,31);
% s(17)='-';s(14)='-';s(11)='-';
% path=strcat(p,s);
% dlmwrite(path,RawData,'precision','%5f','delimiter','\t')
% end
% end
% radar.close();
% clear radar frame
