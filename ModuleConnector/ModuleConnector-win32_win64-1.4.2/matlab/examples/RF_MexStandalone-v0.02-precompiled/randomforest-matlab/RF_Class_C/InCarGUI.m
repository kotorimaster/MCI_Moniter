function varargout = InCarGUI(varargin)
% INCARGUI MATLAB code for InCarGUI.fig
%      INCARGUI, by itself, creates a new INCARGUI or raises the existing
%      singleton*.
%
%      H = INCARGUI returns the handle to a new INCARGUI or the handle to
%      the existing singleton*.
%
%      INCARGUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in INCARGUI.M with the given input arguments.
%
%      INCARGUI('Property','Value',...) creates a new INCARGUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before InCarGUI_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to InCarGUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help InCarGUI

% Last Modified by GUIDE v2.5 13-Apr-2018 16:07:22

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @InCarGUI_OpeningFcn, ...
    'gui_OutputFcn',  @InCarGUI_OutputFcn, ...
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


% --- Executes just before InCarGUI is made visible.
function InCarGUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to InCarGUI (see VARARGIN)

% Choose default command line output for InCarGUI
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes InCarGUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = InCarGUI_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function num_edit1_Callback(hObject, eventdata, handles)
% hObject    handle to num_edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of num_edit1 as text
%        str2double(get(hObject,'String')) returns contents of num_edit1 as a double


% --- Executes during object creation, after setting all properties.
function num_edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to num_edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function num_edit2_Callback(hObject, eventdata, handles)
% hObject    handle to num_edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of num_edit2 as text
%        str2double(get(hObject,'String')) returns contents of num_edit2 as a double


% --- Executes during object creation, after setting all properties.
function num_edit2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to num_edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function num_edit3_Callback(hObject, eventdata, handles)
% hObject    handle to num_edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of num_edit3 as text
%        str2double(get(hObject,'String')) returns contents of num_edit3 as a double


% --- Executes during object creation, after setting all properties.
function num_edit3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to num_edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function num_edit4_Callback(hObject, eventdata, handles)
% hObject    handle to num_edit4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of num_edit4 as text
%        str2double(get(hObject,'String')) returns contents of num_edit4 as a double


% --- Executes during object creation, after setting all properties.
function num_edit4_CreateFcn(hObject, eventdata, handles)
% hObject    handle to num_edit4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function num_edit5_Callback(hObject, eventdata, handles)
% hObject    handle to num_edit5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of num_edit5 as text
%        str2double(get(hObject,'String')) returns contents of num_edit5 as a double


% --- Executes during object creation, after setting all properties.
function num_edit5_CreateFcn(hObject, eventdata, handles)
% hObject    handle to num_edit5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function breath_edit1_Callback(hObject, eventdata, handles)
% hObject    handle to breath_edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of breath_edit1 as text
%        str2double(get(hObject,'String')) returns contents of breath_edit1 as a double


% --- Executes during object creation, after setting all properties.
function breath_edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to breath_edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function breath_edit2_Callback(hObject, eventdata, handles)
% hObject    handle to breath_edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of breath_edit2 as text
%        str2double(get(hObject,'String')) returns contents of breath_edit2 as a double


% --- Executes during object creation, after setting all properties.
function breath_edit2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to breath_edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function breath_edit3_Callback(hObject, eventdata, handles)
% hObject    handle to breath_edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of breath_edit3 as text
%        str2double(get(hObject,'String')) returns contents of breath_edit3 as a double


% --- Executes during object creation, after setting all properties.
function breath_edit3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to breath_edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function breath_edit4_Callback(hObject, eventdata, handles)
% hObject    handle to breath_edit4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of breath_edit4 as text
%        str2double(get(hObject,'String')) returns contents of breath_edit4 as a double


% --- Executes during object creation, after setting all properties.
function breath_edit4_CreateFcn(hObject, eventdata, handles)
% hObject    handle to breath_edit4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function breath_edit5_Callback(hObject, eventdata, handles)
% hObject    handle to breath_edit5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of breath_edit5 as text
%        str2double(get(hObject,'String')) returns contents of breath_edit5 as a double


% --- Executes during object creation, after setting all properties.
function breath_edit5_CreateFcn(hObject, eventdata, handles)
% hObject    handle to breath_edit5 (see GCBO)
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
xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\newradar0704_4.mat'); %%新雷达-4分类
% xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\newoldradar0704_4.mat'); %%新雷达-4分类
% xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\newoldradar0704_6.mat'); %%新雷达-4分类
% xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\newoldradar0704_9.mat'); %%新雷达-4分类
% xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\newoldradar0704_12.mat'); %%新雷达-4分类
% xiu = load('C:\Users\mac\Desktop\ModuleConnector\ModuleConnector-win32_win64-1.4.2\matlab\examples\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\newoldandnewradar0704_4.mat'); %%新雷达-4分类

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
smoothp=zeros(5,5);
smoothp1=zeros(5,5);
smoothp2=zeros(5,5);

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
    
        %     [position, PureData]=fcounting(RawData,batch);
        %     [position]=che_xiuxiuxiu417(RawData,xiu)
        [position]=newradar_xiuxiuxiu704(RawData,xiu) %ori
%         [position]=newradar_xiuxiuxiu7046(RawData,xiu) 
%         [position]=newradar_xiuxiuxiu7049(RawData,xiu) 
%         [position]=newradar_xiuxiuxiu70412(RawData,xiu) 
        %     [position]=che_xiuxiuxiu521bandpass(RawData,xiu)
        %     [position]=che_xiuxiuxiu521nono(RawData,xiu);
        
        smoothp(1:4,:)=smoothp(2:5,:);
        smoothp(5,:)=position;
        presult=mode(smoothp,1);
        %      presult = position;
        %     presult=[1 0 0 0 0];
        set(handles.num_edit1,'string',num2str(presult(1,1)));
        set(handles.num_edit2,'string',num2str(presult(1,2)));
        set(handles.num_edit3,'string',num2str(presult(1,3)));
        set(handles.num_edit4,'string',num2str(presult(1,4)));
        set(handles.num_edit5,'string',num2str(presult(1,5)));
        
        [breath, heart]=heartbeat3(RawData);  %%10列
%         [breath, heart]=heartbeat4(RawData);  %%相关
%         [breath, heart]=heartbeat5(RawData);  %%10列+相关
        
        breath = breath.*60;
        heart = heart.*60;
        smoothp1(1:4,:)=smoothp1(2:5,:);
        smoothp1(5,:)=breath;
        presult_breath=mean(smoothp1);
        
        smoothp2(1:4,:)=smoothp2(2:5,:);
        smoothp2(5,:)=heart;
        presult_heart=mean(smoothp2);
        %       presult_breath = breath;
        %       presult_heart =heart;
        
        for x=1:5
            if presult(1,x)==0
                presult_breath(1,x)=0;
                presult_heart(1,x)=0;
            end
        end
        
        set(handles.breath_edit1,'string',num2str(round(presult_breath(1,1))));
        set(handles.breath_edit2,'string',num2str(round(presult_breath(1,2))));
        set(handles.breath_edit3,'string',num2str(round(presult_breath(1,3))));
        set(handles.breath_edit4,'string',num2str(round(presult_breath(1,4))));
        set(handles.breath_edit5,'string',num2str(round(presult_breath(1,5))));
        
        
        set(handles.heart_edit1,'string',num2str(round(presult_heart(1,1))));
        set(handles.heart_edit2,'string',num2str(round(presult_heart(1,2))));
        set(handles.heart_edit3,'string',num2str(round(presult_heart(1,3))));
        set(handles.heart_edit4,'string',num2str(round(presult_heart(1,4))));
        set(handles.heart_edit5,'string',num2str(round(presult_heart(1,5))));
        
        
        %     x=1/256:1/256:3;
        % %     x=1:1:5000;
        %     axes(handles.axes1);
        %     plot(x,PureData(n,:));
        %     axis([0 3 -3 3]);
        %     xlabel('距离（m）');
        %     ylabel('幅度');
        
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



function heart_edit1_Callback(hObject, eventdata, handles)
% hObject    handle to heart_edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of heart_edit1 as text
%        str2double(get(hObject,'String')) returns contents of heart_edit1 as a double


% --- Executes during object creation, after setting all properties.
function heart_edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to heart_edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function heart_edit2_Callback(hObject, eventdata, handles)
% hObject    handle to heart_edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of heart_edit2 as text
%        str2double(get(hObject,'String')) returns contents of heart_edit2 as a double


% --- Executes during object creation, after setting all properties.
function heart_edit2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to heart_edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function heart_edit3_Callback(hObject, eventdata, handles)
% hObject    handle to heart_edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of heart_edit3 as text
%        str2double(get(hObject,'String')) returns contents of heart_edit3 as a double


% --- Executes during object creation, after setting all properties.
function heart_edit3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to heart_edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function heart_edit4_Callback(hObject, eventdata, handles)
% hObject    handle to heart_edit4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of heart_edit4 as text
%        str2double(get(hObject,'String')) returns contents of heart_edit4 as a double


% --- Executes during object creation, after setting all properties.
function heart_edit4_CreateFcn(hObject, eventdata, handles)
% hObject    handle to heart_edit4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function heart_edit5_Callback(hObject, eventdata, handles)
% hObject    handle to heart_edit5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of heart_edit5 as text
%        str2double(get(hObject,'String')) returns contents of heart_edit5 as a double


% --- Executes during object creation, after setting all properties.
function heart_edit5_CreateFcn(hObject, eventdata, handles)
% hObject    handle to heart_edit5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
