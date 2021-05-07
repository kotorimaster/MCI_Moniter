function hr= efft(hrSignal)

% figure
% plot(hrSignal)

Y = (-2^16/2:2^16/2-1)*(20)/2^16;
fre1=abs(fftshift(fft(hrSignal,2^16)))*1000;
% figure
% plot(Y,fre1);
%     xlabel('ÆµÂÊ/ºÕ×È');
%     ylabel('·ù¶È');
fre2 = fre1(36372:41287,:);
extrMaxValue = fre2(find(diff(sign(diff(fre2)))==-2)+1);
extrMaxIndex = find(diff(sign(diff(fre2)))==-2)+1;
[c,v]=max(extrMaxValue);
f = extrMaxIndex(v);
provalue = 1.1+ 20*f/65536;
hr = provalue*60;