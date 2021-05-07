function Data = newfilter(RawData)
M=0;L=50;K=1;
pg=1;rx_num=2;
RawData=pca_filter_x4(RawData,rx_num,pg,M,L,K);%ÂË²¨
Data=RawData;