function e=xianboz2(x)
 N=length(x);%�źų���
 fs=512;%����Ƶ�� 512
% x1=randn(1,N);%ģ���Ե��ź�
% x2=sin(2*pi*50*[0:N-1]/fs);%50hz��Ƶ
% x=x1+x2;
x1=x;
d=x1;%�����ź�

% randphase=pi*rand;
randphase=pi*0.5;
C=0.4484;
rx1=C*sin(2*pi*50*[0:N-1]/fs+randphase);%�ο��ź�1
rx2=C*cos(2*pi*50*[0:N-1]/fs+randphase);%�ο��ź�2




m=5;%�˲�������
w1=zeros(1,m);%Ȩ1
w2=zeros(1,m);%Ȩ2
y=zeros(1,N);%����Ӧ�˲������
e=zeros(1,N);%����������������˲����
u=1/32;

m=5;
for k=m:1:N-1
    for i=1:1:m
        x1k(i)=rx1(k-m+i);
        x2k(i)=rx2(k-m+i);
        
    end

    sum1=0;
    sum2=0;
    for i=1:1:m
        sum1=sum1+x1k(i)*w1(i);
        sum2=sum2+x2k(i)*w2(i);
    end
    y(k)=sum1+sum2;
    e(k)=d(k)-y(k);
    for j=1:1:m
        w1(j)=w1(j)+2*u*e(k)*x1k(j);
        w2(j)=w2(j)+2*u*e(k)*x2k(j);
    end

end
        
% figure;
% subplot(3,2,1)
% plot(x1)
% title('�������ź�')
% subplot(3,2,2)
% px1=abs(fft(x1));
% plot(fs/N:fs/N:fs/2,px1(1:N/2))
% title('�������ź�Ƶ��')
% subplot(2,2,1)
% plot(x);hold on;
% title('ԭʼ�ź�')
% subplot(2,2,2)
% px=abs(fft(x));
% plot(fs/N:fs/N:fs/2,px(1:N/2))
% title('ԭʼ�ź�Ƶ��')
% subplot(2,2,3)
% plot(e,'r')
% title('ȥ��Ƶ���ź�')
% subplot(2,2,4)
% pe=abs(fft(e));
% plot(fs/N:fs/N:fs/2,pe(1:N/2))
% title('ȥ��Ƶ���ź�Ƶ��')
% 
% a=[1,-2*(1-u*C*C)*cos(2*pi*50/fs),1-2*u*C*C];
% b=[1,-2*cos(2*pi*50/fs),1];
% figure;    
% [h,ww]=freqz(b,a);
% plot((ww/pi)*(fs/2),20*log10(h));
% title('�˲�����������')
% xlabel('Ƶ��(Hz)')
% ylabel('�������ԣ�db��')
