function  [num_people]=signal_refine(a,n)
% signal=zeros(200,1280);
% for i=1:200
%     signal(i,fix(100*sin(0.02*pi*i))+300)=5;
%     signal(i,fix(100*sin(0.05*pi*i))+600)=3;
%     signal(i,fix(100*sin(0.08*pi*i))+900)=2;    
% end
% figure(9);
% surf(signal);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%ED method%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%paramter initiation%
np=1; %默认只有一对天线
num_channel=n;
num_per_line=1280;
%rt=zeros(number_per_line,num_channel);
% rt=rand(5,100)+1;
Ts=1;
Td=15;
Tobs=1280;
% Tobs=1000;
% Ts=0.125;
dbsigma_square=-33;
sigma_square=10^dbsigma_square;
sigma_square_estimate=0.2;
Nsb=floor(Td/Ts);
number_of_bin=fix(Tobs/Td);
Ebin = zeros(num_channel,number_of_bin);
Abin = zeros(num_channel,number_of_bin);

standard1=1;
standard2=0.8;
standard3=0.55;
% rtt162=importdata('C:\Users\Smart\Desktop\4ren\1\404.txt');
% rtt162=importdata('C:\Users\Smart\Desktop\7ren\1\10.txt');
rtt162=a;
% rtt162=importdata('J:\xiuxiuxiu1\open lobby\8ren\1\810.txt');
% rt5=F;
% rt4=rtt3;
% rt4=rtt4;
% rt4=rtt5;
% rt4=rtt6;
% rt4=rtt7;
% rt4=rtt10; %两人换行走
% rt4=rtt11;
% rt4=rtt12;
% rt4=rtt14;
% rt4=rtt15;
% rt4=rtt16;
rt4=rtt162;
% rt4=rtt20;
% rt4=rtt24;
% rt4=rtt27;
% % rt4=signal;
% figure(10)
% surf(rt4);

meanzerorun1=mean(rt4);
one=rt4;
for i=1:n
    one(i,:)=rt4(i,:)-meanzerorun1;
end;
one=abs(one);

rt4=one;

one_refine=one;
for i=1:num_channel
    for j=1:num_per_line
        if(j<400 && j>0 && one_refine(i,j)>1)
            one_refine(i,j)=1;
        elseif(j<800 && j>=400 && one_refine(i,j)>1)
            one_refine(i,j)=1;
        elseif(j<1200 && j>=800 && one_refine(i,j)>1)
            one_refine(i,j)=1;
        else
            
        end
    end
end

% figure(1)
% surf(one_refine);

% for i=120:num_channel
%     for j=1:length(rt4)
%         rt4(i,j)=0;
%     end
% end

% figure(11)
% surf(rt4);
% [m,n]=size(rt4);
[m,n]=size(rt4);
% y = abs(wgn(m,n,dbsigma_square)); 
% w = randn*sigma_square_estimate);
% rs=rt4+y;
rs=rt4;
[m,n]=size(rs);
Ert=rt4.^2;
Erb=rs.^2;

%calculate energy per channel
% S0=zeros(n,num_channel);
% for k = 1:num_channel
%     for i = 1:n
%         S0(1,k)=S0(1,k)+Ert(k,i);
%     end
% end
% 
% sum_S0=sum(S0);
%calculate Ebin and feature vector fk %
for i = 1:num_channel
    for j = 1:number_of_bin 
        for k=1:Nsb
            Ebin(i,j) = Ebin(i,j)+Erb(i,(j-1)*Nsb+k);
            Abin(i,j) = Abin(i,j)+rs(i,(j-1)*Nsb+k);
%             Ebin(i,j)= Ebin(i,j)+Erb((i-1)*Nsb+j,k);
%             Abin(i,k)=Abin(i,k)+rs((i-1)*Nsb+j,k);
        end;
%         Abin(i,j)=Abin(i,j)/Nsb;
    end
end
% Abin_square=Abin.^2;
Abin_square=Abin.^2;

fk=zeros(num_channel,number_of_bin);
for i = 1:m
    for j = 1:number_of_bin 
       % fk(i,j)= (Ebin(i,j)/sigma_square- Nsb)/Abin_square(i,j); %equation(25)
       %fk(i,j)= Ebin(i,j)/Abin_square(i,j);
       fk(i,j)= Ebin(i,j);
    end
end

meany=0.0501;

%equation(27)
person_count=zeros(num_channel,number_of_bin);
% for k = 1:m
%     for i = 1:number_of_bin
% %         person_count(k,i) =person_count(k,i)+fk(k,i)/Abin_square(k,i);
%     person_count(k,i) =person_count(k,i)+fk(k,i);
%     end
%     person_count(k,i) =person_count(k,i)/S0(1,k);
% end
% figure(12);
% % plot(0:(length(Abin_square)-1),Abin_square);
% surf(Abin_square);
% figure(4);
% plot([0:Ts:(rt3_len-1)*Ts],rs);
% figure(6);
% plot(person_count);

%%%%%%%%%%%%%%%%%参照值拟合%%%%%%%%%%%%%%
% x=[2,12,22,32];
% y=[1.4512,0.7273,0.3637,0.1819];
% a=1.669;
% b=-0.06916;
% D_model=zeros(num_channel,number_of_bin);
% for i = 1:m
%     for j = 1:number_of_bin 
%         D_model(i,j)=a*exp(b*j);
%     end
% end
% figure(13);
% surf(D_model);


   

selected_bin=zeros(num_channel,number_of_bin);
for i = 1:m
    for j = 1:number_of_bin 
        if(j<30 && fk(i,j)>standard1 )
            selected_bin(i,j)= fk(i,j);
        elseif(j<=47 && fk(i,j)>standard2 && j>=30)
            selected_bin(i,j)= fk(i,j);
        elseif(j>47 && fk(i,j)>standard3)
            selected_bin(i,j)= fk(i,j);
        else
            selected_bin(i,j)=0;
        end
    end
end

compare_bin=zeros(num_channel,number_of_bin);
for i = 1:m
    for j = 1:number_of_bin 
%         compare_bin(i,j)=selected_bin(i,j)/D_model(i,j);
        compare_bin(i,j)=selected_bin(i,j);
    end
end

% figure(14);
% % plot(compare_bin,'.');  
% surf(compare_bin);

ultimate_bin=zeros(num_channel,number_of_bin);


for i = 1:num_channel
    j=1;
    while(j <=number_of_bin-1)
        sum=0;
        index1=0;
        if(compare_bin(i,j)~=0)
            index1=j;
            while(compare_bin(i,j)~=0 && j <=number_of_bin-1)
                sum = sum+compare_bin(i,j);
                ultimate_bin(i,j)=0;
                j=j+1;
            end
            ultimate_bin(i,index1)=sum;
        end
        j=j+1;
    end
end

% ultimate_bin_bin=zeros(num_channel,number_of_bin);
% for i = 1:m
%     for j = 1:number_of_bin
%         if( ultimate_bin(i,j)<1.5)
%             ultimate_bin_bin(i,j)=round(ultimate_bin(i,j));
%         else
%             ultimate_bin_bin(i,j)=floor(sqrt(ultimate_bin(i,j)));
%         end
%     end
% end
ultimate_bin_bin=zeros(num_channel,number_of_bin);
for i = 1:m
    for j = 1:number_of_bin
        if( ultimate_bin(i,j)>0)
            ultimate_bin_bin(i,j)=1;
        else
            ultimate_bin_bin(i,j)=floor(sqrt(ultimate_bin(i,j)));
        end
    end
end            
            
            

counter=zeros(num_channel,1);
for i = 1:m
    for j = 1:number_of_bin 
        if( ultimate_bin_bin(i,j)>1e-3)
            counter(i,1)=counter(i,1)+ultimate_bin_bin(i,j);
        end
    end
end

%%%%%%计算不为0的区间个数%%%%%%%%%%%%%
counter2=zeros(num_channel,1);
% counter2=0;
for i = 1:num_channel
    for j = 1:number_of_bin 
        if( ultimate_bin_bin(i,j)>1e-3)
%             counter2=counter2+1;
            counter2(i,1)=counter2(i,1)+1;
        end
    end
end

max_number_of_person=max(counter2);
distribute_of_personcount=zeros(max_number_of_person+1,1);
for i=1:length(counter2)
    for j=1:(max_number_of_person+1)
        if(counter2(i)==j-1)
            distribute_of_personcount(j)=distribute_of_personcount(j)+1;
        end
    end
end


        
% figure(15);
% plot(1:(length(Abin_square)),fk,1:(length(Abin_square)),D_model);


%%%%%%%%%%%%%%%目标定位%%%%%%%%%%%%%%%%%%
sum_interval=0;
for i=1:length(counter2)
    sum_inverval=sum_interval+counter2(i,1);
end


max_search=zeros(num_channel,number_of_bin);
search_width=fix(Nsb/10);

A_select=zeros(sum_inverval,Nsb-search_width+1);
% A_select=zeros(num_channel,number_of_bin,Nsb-search_width+1)
number_of_person=0;
% max_person_per_line=max(counter2);
x_co=zeros(sum_inverval,1);
y_co=zeros(sum_inverval,1);
counter5=0;
for i=1:num_channel
    for j=1:number_of_bin
        if(ultimate_bin_bin(i,j)>1e-3)
            counter5=counter5+1;
            x_co(counter5,1)=i;
            y_co(counter5,1)=j;
            number_of_person=number_of_person+1;
            %temp=rs(i,(j-1)*Nsb+1);
            for k=1:(Nsb-search_width+1)
                temp=0;
                for m=1:search_width
                    temp=temp+rs(i,(j-1)*Nsb+m+k);
                end
                A_select(number_of_person,k)=temp;
            end
        end
    end
end

[B,index]=sort(A_select,2,'descend');


counter3=0;
coordinate=zeros(num_channel,length(rs));
% for i=1:num_channel
%     for j=1:number_of_bin
%         if(ultimate_bin_bin(i,j)>1e-3)
%             counter3=counter3+1;
%             coordinate(i,index(counter3,1)+(j-1)*Nsb)=1;
%         end
%     end
% end
for i=1:counter5
    coordinate(x_co(i,1),fix(index(i,1)+(y_co(i,1)-1)*Nsb))=1;
end
        
    

% figure(16);
% % plot([0:Ts:(rt3_len-1)*Ts],coordinate);
% surf(coordinate);
%%%%%%%%%%%%%%%目标定位%%%%%%%%%%%%%%%%%%

% max_search=zeros(num_channel,number_of_bin);
% search_width=fix(Nsb/10);
% 
% A_select=zeros(counter2,Nsb-search_width+1);
% % A_select=zeros(num_channel,number_of_bin,Nsb-search_width+1)
% number_of_person=0;
% % max_person_per_line=max(counter2);
% 
% for i=1:num_channel
%     for j=1:number_of_bin
%         if(ultimate_bin_bin(i,j)>1e-3)
%             number_of_person=number_of_person+1;
%             %temp=rs(i,(j-1)*Nsb+1);
%             for k=1:(Nsb-search_width+1)
%                 temp=0;
%                 for m=1:search_width
%                     temp=temp+rs(i,(j-1)*Nsb+m+k);
%                 end
%                 A_select(number_of_person,k)=temp;
%             end
%         end
%     end
% end
% 
% [B,index]=sort(A_select,2,'descend');
% 
% 
% counter3=0;
% coordinate=zeros(num_channel,length(rs));
% for i=1:num_channel
%     for j=1:number_of_bin
%         if(ultimate_bin_bin(i,j)>1e-3)
%             counter3=counter3+1;
%             coordinate(i,index(counter3,1)+(j-1)*Nsb)=1;
%         end
%     end
% end
% 
% figure(6);
% plot([0:Ts:(rt3_len-1)*Ts],coordinate);


%%%%%%%%%%%%%%%%%%%%%%轨迹追踪%%%%%%%%%%%%%%%%%%%%%%
% signal=zeros(120,1280);
% for i=1:120
%     signal(i,fix(100*sin(0.02*pi*i))+300)=1;
%     signal(i,fix(100*sin(0.05*pi*i))+600)=0.5;
%     signal(i,fix(100*sin(0.08*pi*i))+900)=0.2;    
% end
% figure(9);
% surf(signal);

%%%%%%%%%%%%%%%remove the points which are too close to the other%%%%%%%%%
interval_control=0;
coodinate2=[x_co,y_co];
coodinate3=[x_co,y_co];
sum_per_line=0;
for i=1:(num_channel-1)
    for j=2:counter2(i,1)
        if(coodinate2(sum_per_line+j,2)-coodinate2(sum_per_line+j-1,2)<interval_control)
            coodinate2(sum_per_line+j,2)=0;
        end
    end
    sum_per_line=sum_per_line+counter2(i,1);
end

x_co_refine=coodinate2(:,1);
y_co_refine=coodinate2(:,2);

coordinate_refine=zeros(num_channel,length(rs));
for i=1:counter5
    if(y_co_refine(i,1)>0)
        coordinate_refine(x_co_refine(i,1),fix(index(i,1)+(y_co_refine(i,1)-1)*Nsb))=1;
    end
end

coodinate2_refine=[x_co_refine,y_co_refine];
erro=coodinate3-coodinate2_refine;

% figure(17);
% surf(coordinate_refine);

counter2_refine=zeros(num_channel,1);
% counter2=0;
for i = 1:num_channel
    for j = 1:length(rs)
        if( coordinate_refine(i,j)>1e-3)
            counter2_refine(i,1)=counter2_refine(i,1)+1;
        end
    end
end
max_refine=max(counter2_refine);
%%%%%%%%%%%%%%%%%%%tracking%%%%%%%%%%%%%%%%%%%%
%%%%%%如果将每一行的数据与前一行的每个点之间的距离计算出来，将会是指数级的复杂度%%%%%%%%%%%%%
% arry_of_trajectory

% coordinate_refine(1,:)=0;
coordinate_refine(:,1:10)=0;
coordinate_refine(:,1000:1280)=0;
refine_graph=zeros(num_channel,length(rs));
refine_graph2=zeros(num_channel,length(rs));

for i=1:60
    [coordinate_refine,part_of_trajectory_se]=process_of_tracking2(coordinate_refine);
    % t=process_of_tracking(coordinate_refine);
    refine_graph=refine_graph+part_of_trajectory_se;
end
% figure(32);
% surf(refine_graph);

sum_sum=zeros(num_channel,1);
for i=1:num_channel
    for j=1:length(rs)
        if (refine_graph(i,j)>0)
           sum_sum(i,1)=sum_sum(i,1)+1;
        end
    end
end

max_number_of_person_refine=max(sum_sum);
distribute_of_personcount_refine=zeros(max_number_of_person_refine+1,1);
for i=1:length(sum_sum)
    for j=1:(max_number_of_person_refine+1)
        if(sum_sum(i)==j-1)
            distribute_of_personcount_refine(j)=distribute_of_personcount_refine(j)+1;
        end
    end
end


coordinate_refine2=refine_graph;

for i=1:40
    [refine_graph,part_of_trajectory_se2]=process_of_tracking2(refine_graph);
    % t=process_of_tracking(coordinate_refine);
    refine_graph2=refine_graph2+part_of_trajectory_se2;
end

% figure(33);
% surf(refine_graph2);



sum_sum2=zeros(num_channel,1);
for i=1:num_channel
    for j=1:length(rs)
        if (refine_graph2(i,j)>0)
           sum_sum2(i,1)=sum_sum2(i,1)+1;
        end
    end
end

max_number_of_person_refine2=max(sum_sum2);
distribute_of_personcount_refine2=zeros(max_number_of_person_refine2+1,1);
for i=1:length(sum_sum2)
    for j=1:(max_number_of_person_refine2+1)
        if(sum_sum2(i)==j-1)
            distribute_of_personcount_refine2(j)=distribute_of_personcount_refine2(j)+1;
        end
    end
end

[number,index]=max(distribute_of_personcount_refine);
num_people=index-1;
end

