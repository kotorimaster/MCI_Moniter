function [isReading] = StartStream
ToolkitFunctions.LoadAssemblies();
DeviceList = ToolkitFunctions.DiscoverDevices();
isReading = ToolkitFunctions.SelectDevice(DeviceList{1});
if(~isReading)
    return
end
IRStream = ToolkitFunctions.StartStream();
ToolkitFunctions.SetFirstRange();
end