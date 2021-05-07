function [TempArray, MatImage] = GetThermalData()
    [TempArray, MatImage] = ToolkitFunctions.GetData('Kelvin');
    TempArray = TempArray - 273.15;
end