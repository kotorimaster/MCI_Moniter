function Data = newfilter(RawData)
pg=1;rx_num=2;
RawData=pca_filter_x4(RawData,rx_num,pg);%ÂË²¨
Data=RawData;