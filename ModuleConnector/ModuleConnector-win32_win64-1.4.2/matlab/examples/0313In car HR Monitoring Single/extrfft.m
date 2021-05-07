function hr=extrfft(hrSignal)

% figure
% plot(hrSignal)
% 
% Y = (-2^16/2:2^16/2-1)*(20)/2^16;
% fre1=abs(fftshift(fft(hrSignal,2^16)))*1000;
% figure
% plot(Y,fre1);

hrSignal1=hrSignal(1:100,:);
hrSignal2=hrSignal(90:190, :);
hrSignal3=hrSignal(180:280,:);
hr1= efft (hrSignal1);
hr2= efft (hrSignal2);
hr3= efft (hrSignal3);
A = [hr1,hr2,hr3];
A=sort(A);
diff1=abs(A(3)-A(2));
diff2=abs(A(2)-A(1));
if diff1 >= diff2 
    hr = (A(2)+A(1))/2;
else 
    hr = (A(3)+A(2))/2;
end






