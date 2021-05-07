function  x_fil=kalmanfilter_3(y)
N = length(y);  % Duration of movement
P=0.001;
Q=0.5;
a=1;
H=1;
z=zeros(N,1);
z(1)=y(1);
K=zeros(1,N);
x_pre=zeros(N,1);
x_fil=zeros(N,1);
x_fil(1)=y(1);
x_pre(1)=y(1);
p_fil(1)=0.04;
L=20;
M=5

p=zeros(N,2);
for t=2:N                %%% multiple innovations
    bgn2=max(1,t-M);btm2=t;    
    x_pre(t)=a*x_fil(t-1)+K(bgn2:btm2)*(z(bgn2:btm2)-H*x_pre(bgn2:btm2));
    p_pre(t)=a*p_fil(t-1)*a'+P; 
    K(t)=p_pre(t)*H'*inv(H*p_pre(t)*H'+Q);
    z(t)=y(t);
    x_fil(t)=x_pre(t)+K(t)*(z(t)-H*x_pre(t));
    p_fil(t)=(1-K(t)*H)*p_pre(t);
end
t=1:N;
% figure;hold on;plot(t,z,'g');
% plot(t,x_fil,'r');
% plot(y);
% legend('Filtering','measurement');