function [refine_graph,part_of_trajectory_se]=process_of_tracking2(refine_graph) %number_of_track为设定的追踪次数
Td=15;
lowerlimit=10;
interval_control=5;
row_interval=4*Td; %4
col_interval=15; %10
num_channel=50;
num_per_line=1280;
T=zeros(5*num_channel,2);
co_x_first=0;
co_y_first=0;
counter_1=1;
for i=1:num_channel
    for j=1:num_per_line
        if(refine_graph(i,j)==1 && counter_1==1)
            co_x_first=i;
            co_y_first=j;
            counter_1= counter_1+1;
        end
    end
end

T(1,1)=co_x_first;
T(1,2)=co_y_first;

for i=1:num_channel
    for j=1:num_per_line
        if(refine_graph(i,j)==1 && (abs(i-T(counter_1-1,1))<col_interval) && abs((j-T(counter_1-1,2)))<row_interval)
            T(counter_1,1)=i;
            T(counter_1,2)=j;
            counter_1=counter_1+1;
        end
    end
end


part_of_trajectory=zeros(num_channel,num_per_line);
for i=1:length(T)
    if(T(i,1)~=0 && T(i,2)~=0)
        part_of_trajectory(T(i,1),T(i,2))=1;
    end
end

% figure(18);
% surf(part_of_trajectory);


% figure(19);
% surf(part_of_trajectory_se);


% figure(20);
% surf(part_of_trajectory_se);

refine_graph=refine_graph-part_of_trajectory;

part_of_trajectory_se=zeros(num_channel,num_per_line);
non_zeros=find(part_of_trajectory);
num_of_non_zeros=length(non_zeros);
if(num_of_non_zeros>lowerlimit)
    for i=1:num_channel
        for j=1:num_per_line
            if (part_of_trajectory(i,j)>0)
                part_of_trajectory_se(i,j)=1;
                break
            end
        end
    end
    sum_se=zeros(num_channel,1);
    for i=1:num_channel
        for j=1:num_per_line
            if (part_of_trajectory_se(i,j)>0)
                sum_se(i,1)=sum_se(i,1)+1;
            end
        end
    end
    
    position=0;
    for i=num_channel:-1:1
        if sum_se(i,1)>0;
            position=i;
            break
        end
    end
    
    for i=1:position-1
        for j=1:num_per_line
            if(part_of_trajectory_se(i,j)>0 && sum_se(i+1,1)==0)
                part_of_trajectory_se(i+1,j+1)=1;
            end
        end
    end
end


