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
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global flag1
flag1=1;
% radarlink;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\newxiu_2018816.mat'); %%新雷达-4分类
% xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\newoldradar0704_6.mat'); %%新雷达-4分类
% xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\newoldradar0704_9.mat'); %%新雷达-4分类
% xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\newoldradar0704_12.mat'); %%新雷达-4分类
% xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\newoldandnewradar0704_4.mat'); %%新雷达-4分类
% xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\count_oldandnew4.mat');

%%%%%%%%%%
%xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\zhanshicount_4.mat'); %%新雷达-4分类
% xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\zhanshicount_6.mat'); %%新雷达-4分类


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

% smoothp=zeros(10,5);
% smoothp=zeros(5,5);
% smoothp1=zeros(5,5);
% smoothp2=zeros(5,5);

while(i)
    
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
    if mod(i,201)==0
        position =[];
        %     [position, PureData]=fcounting(RawData,batch);
        %     [position]=che_xiuxiuxiu417(RawData,xiu)
%         size(RawData)
        [people1,PureData, mph1]=newradar_signalprocessing(RawData); 
        set(handles.edit1,'string',num2str(people1));  
        [people2]=newradar_feature(RawData,xiu);   
        set(handles.edit2,'string',num2str(people2));
        
        
        x=0.2+2.8/417:2.8/417:3;   
       axes(handles.axes1);
       plot(x,PureData(100,:));
       line([0.2,3],[mph1,mph1],'color','r');
       axis([0.2 3 -0.01 0.01]);
       xlabel('距离（m）');
       ylabel('幅度');

        
        pause(0.1);
        %     n=n+1;
        if (flag1==0 )%|| n>200
            i=0;
            break;
        end
    end
end


% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global flag1
flag1=0;
