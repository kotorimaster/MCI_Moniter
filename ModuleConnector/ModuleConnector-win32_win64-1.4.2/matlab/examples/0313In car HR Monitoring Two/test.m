clc
close all
clear

a=[2,2,3];
b=[2,4,3];
c=[2,2,3];
d=[a;b;c]
figure(1)
subplot(3,1,1)
plot(a);
subplot(3,1,2)
plot(b);
subplot(3,1,3)
plot(c);


subplot(3,1,1)
plot(b);
subplot(3,1,2)
plot(c);
subplot(3,1,3)
plot(a);
