%%%%%%%%%%%%%%%%%%%��ȡ�����Ѫ���ǲ���  һ��  ���û�ж�ȡ���򷵻�-1%%%%%%%%%%
function [xueyangyihb,xueyangyitime] = oximeter3()
dos('3.bat');
%clc
fidin=fopen('C:\Users\mengyao\Desktop\3\value.txt');                               % ��test2.txt�ļ�

value={};
framnumber = 1;
i=1;
b='';
number = 0;

while ~feof(fidin)
    tline = fgetl(fidin);
    number=number+1;
    if strcmpi('',tline)
        
        value{i}=b;
        i=i+1;
        framnumber = framnumber + 1 ;
        b='';
    else
        
        b=strcat(b,tline);
        
    end
    
end

fclose(fidin);
value=value';
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%ʱ��
fidin=fopen('C:\Users\mengyao\Desktop\3\time.txt');                               % ��test2.txt�ļ�

i=1;

while ~feof(fidin)
    tline = fgetl(fidin);
    time(i,:)=[tline(9) tline(10) tline(11) tline(12) tline(14) tline(15) tline(17) tline(18) tline(20) tline(21) ];
    i=i+1;
end
fclose(fidin);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%ʱ��

valuelength = size(value,1);
test = value(valuelength-99:valuelength);     %ÿ��ȡ�����ʮ��

timelength = size(time,1);
timebox = time(timelength-99:timelength,:);   %ÿ��ȡ�����ʮ��

count = 0; %��¼�����50��ȡ�����ʵĴ���
xueyangyitime=[];
xueyangyihb=[];
xueyangyihb=-1;  %��������ʮ����û���ҵ����ʼ���ʱ�䣬�򷵻�-1
xueyangyitime=-1;
for i=1:100
    if  (~isempty(strfind(test{i},'aa 55'))) &&(~isempty(strfind(test{i},'0f 08')))
        count=count+1;
        enen = test{i};
        idx=strfind(enen,'0f 08');
        newenen=enen(idx(1):size(enen,2));
        idx=strfind(newenen,' 01 ');
        
        if (numel(idx)==0)
            xueyangyihb=-1;
            continue;
        end        
  
        heartbeat=[newenen(idx(1)+7) newenen(idx(1)+8)];
        if(   ('0'<=heartbeat(1))&&(heartbeat(1)<='9')    )  &&  (      ('0'<=heartbeat(2))&&(heartbeat(2)<='9')    ||       ('a'<=heartbeat(2))&&(heartbeat(2)<='f')       )
            heartbeat=hex2dec(heartbeat);
            xueyangyitime(count)=str2num([timebox(i,7),timebox(i,8),timebox(i,9),timebox(i,10)]);
            xueyangyihb(count)=heartbeat;
        end              
    end     
end

%pause(2)
end

