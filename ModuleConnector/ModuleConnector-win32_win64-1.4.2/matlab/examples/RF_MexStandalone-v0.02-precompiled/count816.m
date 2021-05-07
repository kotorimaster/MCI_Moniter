function varargout = count816(varargin)
% COUNT816 MATLAB code for count816.fig
%      COUNT816, by itself, creates a new COUNT816 or raises the existing
%      singleton*.
%
%      H = COUNT816 returns the handle to a new COUNT816 or the handle to
%      the existing singleton*.
%
%      COUNT816('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in COUNT816.M with the given input arguments.
%
%      COUNT816('Property','Value',...) creates a new COUNT816 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before count816_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to count816_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help count816

% Last Modified by GUIDE v2.5 16-Aug-2018 19:50:42

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @count816_OpeningFcn, ...
                   'gui_OutputFcn',  @count816_OutputFcn, ...
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


% --- Executes just before count816 is made visible.
function count816_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to count816 (see VARARGIN)

% Choose default command line output for count816
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes count816 wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = count816_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function edit1_Callback(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1 as text
%        str2double(get(hObject,'String')) returns contents of edit1 as a double


% --- Executes during object creation, after setting all properties.
function edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit2_Callback(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit2 as text
%        str2double(get(hObject,'String')) returns contents of edit2 as a double


% --- Executes during object creation, after setting all properties.
function edit2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
xiu = load('F:\radar\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\newxiu_2018920.mat'); %%新雷达-7分类

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
global flag1
flag1=1;
i=1;
RawData=[];

while(1)
    
    % Peek message data float
    numPackets = radar.bufferSize();
    
    if numPackets> 0;
        % Get frame (uses read_message_data_float)
        [frame, ctr] = radar.GetFrameNormalized();
        RawData=[RawData;frame'];
        i=i+1;
    end
        
%         %s=datestr(now,'yyyymmddHHMMSSFFF');
%         s=datestr(now,'HHMMSS.FFF');    %%%%%%%%%%%%%%%%%得到读取这一帧的时间
%         
%         timestamp(i)=str2num(s);
%         timestamp = timestamp';
%         i=i+1;
%     end
    people1 = 0;
    people2 = 0;
    if mod(i,201)==0
        [people1,PureData, mph1]=newradar_signalprocessing(RawData); 
        set(handles.edit1,'string',num2str(people1));  
        [people2]=newradar_feature(RawData,xiu); 
        if people1 >= 7
        people2 = people1;
        end
        set(handles.edit2,'string',num2str(people2));
        
        
        x=0.2+2.8/417:2.8/417:3;   
       axes(handles.axes1);
       plot(x,PureData(100,:));
       line([0.2,3],[mph1,mph1],'color','r');
       axis([0.2 3 -0.003 0.003]);
       xlabel('距离（m）');
       ylabel('幅度');
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
global flag1
flag1=0;
