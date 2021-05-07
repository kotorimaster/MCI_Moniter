%3s时间窗
%取畜值?蹋?s取一个模极大值，求?个极大值
function [rr,addr]=qrs(s)
mml=512;
n=fix(length(s)/mml);
s=s';
%去基线漂移
b = fir1(100,0.02,'high',kaiser(101,2));
s=filtfilt(b,1,s);
[va,vb]=max(abs(s));
if s(vb)<0
    s=-1*s;
end
%去工频干扰
x=xianboz2(s);
%5尺度的小波分?
%B小波的低通分解滤波?
low=[0,0.125,0.375,0.375,0.125,0];
%B小波的高通分解滤波?inversed)
high=[0.0061,0.0869,0.5798,-0.5798,-0.0869,-0.0061];
%A'trous alogrithm
low2=[0,0,0.125,0,0.375,0,0.375,0,0.125,0,0];
high2=[0.0061,0,0.0869,0,0.5798,0,-0.5798,0,-0.0869,0,-0.0061];

low4=[0,0,0,0,0.125,0,0,0,0.375,0,0,0,0.375,0,0,0,0.125,0,0,0,0];
high4=[0.0061,0,0,0,0.0869,0,0,0,0.5798,0,0,0,-0.5798,0,0,0,-0.0869,0,0,0,-0.0061];

N=zeros(1,7);
low8=[0,N,0.125,N,0.375,N,0.375,N,0.125,N,0];
high8=[0.0061,N,0.0869,N,0.5798,N,-0.5798,N,-0.0869,N,-0.0061];

M=zeros(1,15);
low16=[0,M,0.125,M,0.375,M,0.375,M,0.125,M,0];
high16=[0.0061,M,0.0869,M,0.5798,M,-0.5798,M,-0.0869,M,-0.0061];
%一层分?
%d1(k)
d1=conv(x,high);  
a1=conv(x,low);
%d2(k)
%?惴纸?
d2=conv(a1,high2);
a2=conv(a1,low2); %%a2信号比S偏移的点??.5  
%d3(k)
%?惴纸?
d3=conv(a2,high4);
a3=conv(a2,low4);
%d4(k)
%四层分?
d4=conv(a3,high8);
a4=conv(a3,low8);
%d5(k)
%五层分?
d5=conv(a4,high16);
a5=conv(a4,low16);
n5=78:length(d5);
[d55,n55]=sigshift(d5,n5,77);
figure(1)
subplot(511);plot(d1);
subplot(512);plot(d2);
subplot(513);plot(d3);
subplot(514);plot(d4);
subplot(515);plot(d5);

c=[];
for i=1:length(d5)
    c=[c abs(d5(i))];
end
smax=zeros(1,n);
for j=1:n  
      smax(j)=c(mml*(j-1)+1);
      for i=mml*(j-1)+1:mml*j
          if c(i)>smax(j)
              smax(j)=c(i);
          end
      end
end 
thqrs=0.55*mean(smax);
thse=0.2*mean(smax);%根据具体情况确定阈值
%?≧波
addr=[];
location=1;
i=1;
interval=fix(300*mml/1000);
while(i<length(d5))

     if d5(i)>=thqrs
         location=i;
        for j=1:30
            if i+j<length(d5)
                if d5(i+j)*d5(i+j+1)<0 & d5(i+j)>d5(i+j+1)
                  location=i+j;
                  break;
                end    
            end
        end  
         addr=[addr location];
         i=location+interval;   
      
    else i=i+1;
    end
end
%确定QRS波起?
addq=[];
for i=1:length(addr)
    
    for k=addr(i)-3:-1:1
         if c(k)<thse&c(k)>=c(k-1)
                 if k-78<1
                     addq=[addq 0];
                 else
                     addq=[addq k-78];
                 end
                 break;
         end
    end
end
% r=length(addr);

%确定QRS波终?
adds=[];
for i=1:length(addr)
    for k=addr(i)+3:addr(i)+100
        if c(k)<thse & c(k)>=c(k+1)   
                if k-78>length(x)
                     adds=[adds 0];
                else
                adds=[adds k-78];   
                end
                break;
        end
    end
end 
%修?波位置
addr=addr-78;
len_x=numel(x);
for i=1:length(addr)
    if addr(i)>0&addr(i)<=len_x
        str=max(1,addr(i)-2);
        tnd=min(length(x),addr(i)+2);
        rmax=x(addr(i));
        for j=str:tnd
            if x(j)>rmax
                addr(i)=j;
            end
        end
    end
end
rw=zeros(1,length(x));
r=0;
for i=1:length(addr)
    if addr(i)<1||addr(i)>length(x)
        addr(i)=0;
    else
        rw(addr(i))=x(addr(i)); 
        r=r+1;
    end
end

qw=zeros(1,length(x));
for i=1:length(addq)
       if addq(i)>0
       qw(addq(i))=x(addq(i)); 
       end
end
sw=zeros(1,length(x));
for i=1:length(adds)
    if adds(i)>0
        sw(adds(i))=x(adds(i)); 
    end
end


%确定J?
e=zeros(1,length(d5)-1);
for i=1:length(d5)-1
    e(i)=d5(i+1)-d5(i);
end
dpk=max(e)/3;
jpoint=[];
for i=1:length(adds)
    if adds(i)>0
    for j=1:50
       if e(adds(i)+j+78)<dpk
           if adds(i)+j<length(x)
              jpoint=[jpoint adds(i)+j];
           else jpoint=[jpoint 0];
           end
          break;
       end
    end
    else jpoint=[jpoint 0];
    end
end
jw=zeros(1,length(x));
for i=1:length(jpoint)
    if jpoint(i)>0
       jw(jpoint(i))=x(jpoint(i));
    end
end

%?═波
addt=[];
for i=1:length(jpoint)
    if jpoint(i)>0
       tmax=x(jpoint(i));
       location=jpoint(i);
       if length(x)-jpoint(i)<10
            addt=[addt 0];
       else
            for j=1:50
              if jpoint(i)+j<=length(x)
                 if x(jpoint(i)+j)>tmax
                     tmax=x(jpoint(i)+j);
                    location=jpoint(i)+j;
                 end
              end
            end
            addt=[addt location];
       end
      
    else  addt=[addt 0];
    end
end
tw=zeros(1,length(x));
t=0;
for i=1:length(addt)
    if addt(i)>0
        tw(addt(i))=x(addt(i));
        t=t+1;
    end
end
% t=length(addt);
% if addt(length(addt))>0
% s0=addt(length(addt))+10;
% else s0=sqrs(length(sqrs))-10;
% end

%RR间期
rr=zeros(1,length(addr)-1);
for i=1:length(addr)-1
    rr(i)=addr(i+1)-addr(i);
end
thrr=round(0.4*mean(rr));
% %?≒波
% opoint=[];
% for i=1:length(addq)
%     %确定P波?馇鋄str，tnd]
%     if i==1
%     str=max(1,sqrs(i)-thrr);
%     else str=max(addt(i-1)+10,sqrs(i)-thrr);
%     end
%     tnd=sqrs(i)-1;
% %确定P波极值?
%     for j=str:tnd
%        if d55(j)*d55(j+1)<=0
%            opoint=[opoint j];
%        end
%     end  
% end
% 
% opw=zeros(1,length(x));
% for i=1:length(opoint)
%     opw(opoint(i))=x(opoint(i));
% end
% 
figure(2)
plot(x);hold on;
plot(rw,'r*');
% plot(sn,'m');
plot(qw,'g*');
plot(sw,'m*');
plot(jw,'k*');
plot(0.6*mean(smax)*ones(1,length(x)));
plot(0.85*mean(smax)*ones(1,length(x)));
plot(mean(smax)*ones(1,length(x)));
plot(max(smax)*ones(1,length(x)));
% plot(tw,'r*');
% plot(opw,'m*');
% figure(3)
% plot(d3);hold on;plot(rw,'r*');
