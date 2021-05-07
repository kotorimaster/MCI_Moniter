classdef ToolkitFunctions
    %TOOLKITFUNCTIONS Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
       
    end
    
    methods(Static)
        
        %Loads in .DLL files required to interface with the camera
        function LoadAssemblies()
            global asm;
            %Add the dll's needed and any other import required
            if ~IsAssemblyAdded('IRAccessNG.dll')
                if ~isdeployed
                    %Get the Current path and load the assembly
                    S = mfilename('fullpath');
                    R = mfilename;
                    L= length(R);
                    cPath = S(1:end-L);
                    asm = NET.addAssembly(fullfile(cPath, 'OpenAccess64', 'IRAccessNG.dll'));
                else
                    asm = NET.addAssembly('C:\Program Files\FlukeStreamingGUI\application\OpenAccess64\IRAccessNG.dll');
                end
            end
            if ~IsAssemblyAdded('System.Drawing')
                NET.addAssembly('System.Drawing');
            end
            
            NET.addAssembly('System.Windows.Forms');
            
            import Fluke.Thermography.IRAccess.Streaming.*
            import Fluke.Thermography.IRAccess.*
            import Fluke.Thermography.IRAccess.OAImageImplementation.*
            import System.String
            import System.Drawing.*
            import System.Windows.Forms.*
            
        end
        
        %Discovers Fluke Thermal Imagers that are on the same network as the current machine. 
        %Returns an array of the names of the discovered Fluke Thermal Imagers as well
        %as an interface used to communicate with the cameras.
        function deviceList = DiscoverDevices()    
            %start the engine manager
            Fluke.Thermography.IRAccess.Streaming.StreamingCameraEngine.Start();
            pause(0.05); 
            global EngMgr;
            EngMgr = Fluke.Thermography.IRAccess.Streaming.StreamingCameraEngine.Instance; 
            %task of finding device, this can be run on its own thread
            %for now just search until one device is found.
            DeviceCollection = EngMgr.GetCurrentGevCameras();
            while DeviceCollection.Count == 0
                %disp("Searching");
                DeviceCollection = EngMgr.GetCurrentGevCameras();
                pause(0.02);
            end
            %update the list
            dcEnum = DeviceCollection.GetEnumerator();
            newstring = {}; 
            while dcEnum.MoveNext
                newitem = {char(dcEnum.Current.CameraSerial)};   
                newstring = {newitem{:}; newstring{:}}; %put on top 
                %disp(newstring);
            end
            deviceList = newstring;
        end
        
        %Sends a command to the camera interface to select the camera with 
        %the given serial number. Returns a Boolean to determine success.
        function success = SelectDevice(camSerial)
            global EngMgr;
            EngMgr.SelectDevice(camSerial);
            pause(0.05);
            success = EngMgr.IsCameraSelected();
        end
        
        %Connect to the camera and begin streaming data
        function cameraStream = StartStream()
            global CameraStream;
            global EngMgr;
            engine = EngMgr.Engine;
            Fluke.Thermography.IRAccess.Streaming.StreamSource.Open(engine);
            pause(0.05);
            CameraStream = Fluke.Thermography.IRAccess.Streaming.StreamSource.Instance;
            %CameraStream.RegisterFrameCallback(@FrameCallback);
            CameraStream.Subscribe(Fluke.Thermography.IRAccess.Streaming.EventElements.All);
            CameraStream.StartStaticFrameEventQueue();
            cameraStream = CameraStream;
        end
        
        %MATLAB does not natively support .net bitmaps.
        %This function performs some data manipulation on the bits
        %and returns an image that can be displayed on an axes
        % --- .net bitmap to matlab image
        function img = Net2MatImage(bitmap)
            bmp = bitmap;
            w = bmp.Width;
            h = bmp.Height;

            % lock bitmap into memory for reading
            bmpData = bmp.LockBits(System.Drawing.Rectangle(0, 0, w, h), ...
            System.Drawing.Imaging.ImageLockMode.ReadOnly, bmp.PixelFormat);

            % get pointer to pixels, and copy RGB values into an array of bytes
            num = abs(bmpData.Stride) * h;
            bytes = NET.createArray('System.Byte', num);
            System.Runtime.InteropServices.Marshal.Copy(bmpData.Scan0, bytes, 0, num);

            % unlock bitmap
            bmp.UnlockBits(bmpData);

            % cleanup
            clear bmp bmpData num

            % convert to MATLAB image
            bytes = uint8(bytes);
            bb = bytes(1:4:end);
            gg = bytes(2:4:end);
            rr = bytes(3:4:end);
            b = reshape(bb, [w,h])';
            g = reshape(gg, [w,h])';
            r = reshape(rr, [w,h])';
            img = cat(3,r,g,b);
        end
        
        %Returns a 2D Matrix of Temperature Data and an image that can be
        %displayed on an axes
        function [TempArray, MatImage] = GetData(temperatureUnits)
            global CameraStream;
            currentFrame = CameraStream.GetCurrentDataFrame();
            while isempty(currentFrame)
               currentFrame = CameraStream.GetCurrentDataFrame();
            end
            
            TempArray = transpose(single(currentFrame.TemperatureData_Celcius));
            
            if temperatureUnits == "Fahrenheit"
                TempArray = TempArray * 1.8 + 32;
            end
            
            if temperatureUnits == "Kelvin"
                TempArray = TempArray + 273.15;
            end
                
            Image = currentFrame.IR_Bitmap;
            MatImage = ToolkitFunctions.Net2MatImage(Image);
            %imshow(MatImage);
        end
        
        %Stops the stream and closes the connection to the camera
        function StopStream()
            global CameraStream;
            global EngMgr;
            Fluke.Thermography.IRAccess.Streaming.StreamSource.Close();
            CameraStream.Close();
            disp(EngMgr.IsCameraSelected());
            EngMgr.CloseCameraConnection();
            disp(EngMgr.IsCameraSelected());
            clear CameraStream;
            clear EngMgr;
            Fluke.Thermography.IRAccess.Streaming.StreamingCameraEngine.Stop();
            drawnow;
            pause(0.05);
        end
        
        %Sends a command to the camera to save a .IS2 image to disk
        function CaptureImage(path)
            global CameraStream;
            CameraStream.ExecuteCaptureImage(path, false);
        end
        
        %Sends a command to the camera to manually fire a NUC
        function FireNUC()
            global CameraStream;
            CameraStream.FireFineOffsets();
        end
        
        %Sends a command to the camera to disable the NUC functionality
        function DisableNUC()
            global CameraStream;
            CameraStream.DisableFineOffsets();
        end
        
        %Sends a command to the camera to enable the NUC functionality
        function EnableNUC()
            global CameraStream;
            CameraStream.EnableFineOffsets();
        end
        
        %Sends a command to the camera to adjust the focus distance in mm
        function AdjustFocus(distance)
            global CameraStream;
            CameraStream.SetFocusDistance(distance);
        end
        
        %Sends a command to the camera to set the range to -4°F-176°F
        function SetFirstRange()
            global CameraStream;
            CameraStream.SetFirstRange();
        end
        
        %Sends a command to the camera to set the range to -4°F-2192°F
        function SetSecondRange()
            global CameraStream;
            CameraStream.SetSecondRange();
        end
        
        %Sends a command to the camera to configure the Emissivity and Transmission
        %Coefficients as well as the Background Temperature 
        function SetEBT(Emissivity, BGTemp, TempUnits, Transmission)
            global CameraStream;
            if TempUnits == "Celsius"
                units = Fluke.Thermography.IRAccess.TemperatureUnit.CELSIUS;
            end
            if TempUnits == "Fahrenheit"
                units = Fluke.Thermography.IRAccess.TemperatureUnit.FAHRENHEIT;
            end
            if TempUnits == "Kelvin"
                units = Fluke.Thermography.IRAccess.TemperatureUnit.KELVIN;
            end
            
            CameraStream.SetEBT(Emissivity, BGTemp, units, Transmission);
        end
        
        %Returns a boolean value that is true when the temperature crosses
        %a desired threshold. Also returns the min and max values of the
        %array
        function [alarm, minValue, maxValue] = TempAlarm(TempArray, minTempThreshold, maxTempThreshold)
            minValue = double(min(TempArray, [], 'all'));
            maxValue = double(max(TempArray, [], 'all'));
            minBool = lt(minValue, minTempThreshold);
            maxBool = gt(maxValue, maxTempThreshold);
            if minBool | maxBool
                alarm = true;
            else
                alarm = false;
            end
        end
        
        %Returns the minimum and maximum values of an array
        function [minValue, maxValue] = GetMinMax(TempArray)
            minValue = double(min(TempArray, [], 'all'));
            maxValue = double(max(TempArray, [], 'all'));
        end
        
        %Sends a command to the camera to save a .IS3 file to disk
        function RecordMovie(filePath, filePrefix, movieLength) 
            global CameraStream;
            customRecordingSettings = Fluke.Thermography.IRAccess.Streaming.RecordingSettings(filePath, filePrefix, movieLength, false);
            CameraStream.MovieRecordingSettings = customRecordingSettings;
            CameraStream.ExecuteVideoRecording();
        end
        
        %Allows the user to capture a series of images at a specified
        %interval starting when the Boolean input is true
        function BooleanTrigger(filePath, interval, numCaptures, enableIn)
            if enableIn
                interval = interval/1000.0;
                booleanTriggerTimer = timer;
                booleanTriggerTimer.Name = 'Boolean Timer';
                booleanTriggerTimer.TimerFcn = {@ToolkitFunctions.TriggerCallback, filePath};
                booleanTriggerTimer.ExecutionMode = 'fixedSpacing';
                booleanTriggerTimer.Period = interval;
                booleanTriggerTimer.TasksToExecute = numCaptures;
                booleanTriggerTimer.StopFcn = @(src,~) delete(src);
                start(booleanTriggerTimer);
            end
            
        end
        
        %Allows the user to capture a series of images at a specified
        %interval starting when the temperature crosses a given threshold
        function triggerActivated = TempTrigger(filePath, interval, numCaptures, minTempThreshold, maxTempThreshold, tempArray)
            minValue = double(min(tempArray, [], 'all'));
            maxValue = double(max(tempArray, [], 'all'));
            minBool = lt(minValue, minTempThreshold);
            maxBool = gt(maxValue, maxTempThreshold);
            if minBool | maxBool
                interval = interval/1000.0;
                tempTriggerTimer = timer;
                tempTriggerTimer.TimerFcn = {@ToolkitFunctions.TriggerCallback, filePath};
                tempTriggerTimer.ExecutionMode = 'fixedSpacing';
                tempTriggerTimer.Period = interval;
                tempTriggerTimer.TasksToExecute = numCaptures;
                tempTriggerTimer.StopFcn = @(src,~) delete(src);
                start(tempTriggerTimer);
                triggerActivated = true;
            else
                triggerActivated = false;
            end
            
        end
        
        %Allows the user to capture a seris of images at a specified
        %interval starting a specified amout of time after the function is
        %called
        function RelativeTimeTrigger(filePath, interval, numCaptures, numMilliSecondsToWait)
            interval = interval/1000.0;
            delay = numMilliSecondsToWait/1000.0;
            relativeTimer = timer;
            relativeTimer.Name = 'Relative Timer';
            relativeTimer.StartDelay = delay;
            relativeTimer.TimerFcn = {@ToolkitFunctions.TriggerCallback, filePath};
            relativeTimer.ExecutionMode = 'fixedSpacing';
            relativeTimer.Period = interval;
            relativeTimer.TasksToExecute = numCaptures;
            relativeTimer.StopFcn = @(src,~) delete(src);
            start(relativeTimer);
        end
        
        %Allows the user to capture a series of images at a specified
        %interval starting at the given time
        function AbsoluteTimeTrigger(filePath, interval, numCaptures, startTime)
            interval = interval/1000.0;
            absoluteTimer = timer;
            absoluteTimer.Name = 'Absolute Timer';
            absoluteTimer.TimerFcn = {@ToolkitFunctions.TriggerCallback, filePath};
            absoluteTimer.ExecutionMode = 'fixedSpacing';
            absoluteTimer.Period = interval;
            absoluteTimer.TasksToExecute = numCaptures;
            absoluteTimer.StopFcn = @(src,~) delete(src);
            startat(absoluteTimer,datevec(datetime(startTime)));
        end
        
        %Internal function used in the trigger functions
        function TriggerCallback(src, event, filePath)
            ToolkitFunctions.CaptureImage(filePath);
        end
        
        %Creates a mask by drawing a filled in polygon with vertices at the
        %input coordinates. This mask is then used to determine whether or
        %not a given point in the temperature data array is within the
        %desired ROI. Points within the ROI remain unchanged while points
        %outside the ROI have their value changed to -500000. This 2D
        %matrix is then returned. This is useful if the actual indices of
        %the ROI are required.
        %
        %This function also returns a 1D array that contains only the
        %temperature elements that are within the ROI. This enables easy
        %manipulation on the ROI
        function [maskedData, TempArray] = GetROI(TempArray, xPoints, yPoints)
            numRows = size(TempArray,1);
            numCols = size(TempArray,2);
            ROIMask = poly2mask(xPoints, yPoints, numRows, numCols);
            maskedLocations = find(~ROIMask);
            maskedData = TempArray(ROIMask);
            TempArray(maskedLocations) = -500000;
        end
        
        
    end
end

