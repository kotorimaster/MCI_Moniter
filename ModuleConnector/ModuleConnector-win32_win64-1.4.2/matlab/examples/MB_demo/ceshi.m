rx_num=2;  %%�״�����
pg=1;      %%��������Ƶ�� --- X4
pg2=1;
M=10;L=50;K=70;
% PureData1=pca_filter_x4(radar1,rx_num,pg,M,L,K);
[br_s2,hr_s2]=respiration_multi2(pd2);
% X=size(pd2,1);
% Y=size(pd2,2);
% Zmax=max(max(pd2));
% Zmin=min(min(pd2));  
% x=[0:X-1];
% y=[0:Y-1];
% figure;
% mesh(y,x,pd2); 
% axis([0 Y-1 0 X-1 Zmin Zmax]);%�޶���ʾ�ķ�Χ  
% xlabel('range');
% ylabel('time');
% zlabel('amplitude');
% title('PureData1');