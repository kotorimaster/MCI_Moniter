function varargout = realtime_counting(varargin)
% REALTIME_COUNTING MATLAB code for realtime_counting.fig
%      REALTIME_COUNTING, by itself, creates a new REALTIME_COUNTING or raises the existing
%      singleton*.
%
%      H = REALTIME_COUNTING returns the handle to a new REALTIME_COUNTING or the handle to
%      the existing singleton*.
%
%      REALTIME_COUNTING('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in REALTIME_COUNTING.M with the given input arguments.
%
%      REALTIME_COUNTING('Property','Value',...) creates a new REALTIME_COUNTING or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before realtime_counting_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to realtime_counting_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help realtime_counting

% Last Modified by GUIDE v2.5 22-Nov-2017 17:22:13

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @realtime_counting_OpeningFcn, ...
                   'gui_OutputFcn',  @realtime_counting_OutputFcn, ...
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


% --- Executes just before realtime_counting is made visible.
function realtime_counting_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to realtime_counting (see VARARGIN)

% Choose default command line output for realtime_counting
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes realtime_counting wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = realtime_counting_OutputFcn(hObject, eventdata, handles) 
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


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global flag1 
flag1=1;
% % radarlink;
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xiu = load('C:\Users\mac\Desktop\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\model_openlobby.mat');
% xiu = load('C:\Users\mac\Desktop\RF_MexStandalone-v0.02-precompiled\randomforest-matlab\RF_Class_C\model_queue.mat');
try
    radar.Close();
catch me
end
clc;
%File Directory&Name of FTDI Cable,Radar Board, and Radar Chip
radarlib = 'C:\Program Files\Novelda\Radarlib3_API\';
%radarlib = 'D:\Program Files\Novelda\Radarlib3_API\';
asmInfor = NET.addAssembly([radarlib,'Radarlib3.NET.dll']);
portname = 'FTx232H!Serial No: (FT0JRHE2)!NVA-R661!NVA6201';
% portname = 'FTx232H!Serial No: (FTY2IQUX)!NVA-R661!NVA6201';
%Parameter Setting
FrameStitchnum=5;
Iterationsnum=10;
MClkDivnum=0;
PulsesPerStepnum=10;
PGSelectnum=5;
DACStepFinenum=4;
SampleDelaynum=4*10^(-9);
Variables = containers.Map;
Variables('FrameStitch') = FrameStitchnum;
Variables('Iterations')=Iterationsnum;
Variables('MClkDiv')=MClkDivnum;
Variables('PulsesPerStep')=PulsesPerStepnum;
Variables('PGSelect')=PGSelectnum;
Variables('DACStepFine')=DACStepFinenum;
Variables('SampleDelay')=SampleDelaynum;
%Radar Connect
radar = NoveldaAPI.Radarlib3Wrapper.RadarWrapper;

radar.Open(portname);

    
%Parameter Update
varlist = keys(Variables);
for n=1:length(Variables)
    radar.TryUpdateChip(char(varlist(n)),Variables(char(varlist(n))));
end

%Measure Timeing Delay
radar.ExcecuteAction('MeasureAll');
SpeedOfLight=3*10^8;
Resolution=radar.SamplerResolution;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
bitch=200;
RawData=[];
people1=0;
% people2=0;
% r2=zeros(bitch,256*FrameStitchnum);
% T=0;
% distance=0;
% dist=zeros(1,20);
% wh=zeros(1,bitch);
i=1;
while(i)
    %Receive Raw Data
    for DataCursor=1:1:bitch
        RawData(DataCursor,:)=double(radar.GetFrameNormalizedDouble());
    end
   [people1 input_my]=realtime_countingtry(RawData,xiu)
   set(handles.edit1,'string',num2str(people1));  

   
   pause(1);
  if flag1==0
      i=0;
      break;
  end
end

% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global flag1
flag1=0;