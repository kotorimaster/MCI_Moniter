function varargout = multi_breath(varargin)
% MULTI_BREATH MATLAB code for multi_breath.fig
%      MULTI_BREATH, by itself, creates a new MULTI_BREATH or raises the existing
%      singleton*.
%
%      H = MULTI_BREATH returns the handle to a new MULTI_BREATH or the handle to
%      the existing singleton*.
%
%      MULTI_BREATH('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in MULTI_BREATH.M with the given input arguments.
%
%      MULTI_BREATH('Property','Value',...) creates a new MULTI_BREATH or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before multi_breath_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to multi_breath_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help multi_breath

% Last Modified by GUIDE v2.5 04-May-2018 20:47:07

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @multi_breath_OpeningFcn, ...
                   'gui_OutputFcn',  @multi_breath_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before multi_breath is made visible.
function multi_breath_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to multi_breath (see VARARGIN)

% Choose default command line output for multi_breath
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes multi_breath wait for user response (see UIRESUME)
% uiwait(handles.figure1);
set(handles.text1,'string','0'); 
set(handles.text2,'string','0'); 

% --- Outputs from this function are returned to the command line.
function varargout = multi_breath_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%add paths
addpath('../../../matlab/');
addpath('../../../include/');
addpath('../../../lib64/');
addpath('../');
Lib = ModuleConnector.Library;
% Input parameters
COM = 'COM7';
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
while (1)
    % Peek message data float
    numPackets = radar.bufferSize();
    
    if numPackets> 0;
        % Get frame (uses read_message_data_float)
        [frame, ctr] = radar.GetFrameNormalized();
        RawData=[RawData;frame'];
        i=i+1;
    end
    if mod(i,150)==0
        tic
        PureData=pca_filter_x4(RawData,rx_num,pg,M,L,K);
        size(PureData)
        [br_s,hr_s]=respiration_multi2(PureData);
        smoothp(1:4,:)=smoothp(2:5,:);
        smoothp(5,:)=br_s;
        br_s1=mean(smoothp);  
%         br_s1 = br_s;
        smoothp1(1:4,:)=smoothp1(2:5,:);
        smoothp1(5,:)=hr_s;
        hr_s1=mean(smoothp1);
%         hr_s1 = hr_s;
        set(handles.text2,'string',num2str(round(br_s1))); 
        set(handles.text1,'string',num2str(round(hr_s1))); 
        toc
        pause(0.1)
        i=1;
        RawData=[];
    end
      if flag1==0
      break;
     end
end

% Stop streaming.
radar.stop();
% Output short summary report.
framesRead = i;
totFramesFromChip = ctr;

FPS_est = framesRead/tspent;

framesDropped = ctr-i;
radar.close();
clear radar frame


% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

flag1=0;
