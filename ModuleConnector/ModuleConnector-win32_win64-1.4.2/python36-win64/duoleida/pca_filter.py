#-*-coding:utf-8 -*-
import scipy.io as sio
import numpy as np
from numpy import *
def p_f(RawData,M,L):
    c=RawData.shape#数组维度
    FrameStitchnum=int(c[-1]/156)
    SpeedOfLight=3*10^8
    Resolution=0.006430041
    Fs=SpeedOfLight/(Resolution*2)
    #########带通滤波器##################
    load_bf=sio.loadmat('D:/lab/radar/ModuleConnector/ModuleConnector-win32_win64-1.4.2/python36-win64/duoleida/BandFilter_3.mat')
    BanFilter=load_bf['bandfilter']
    BanFilter2=np.array(BanFilter)
    BanFilter3=np.reshape(BanFilter2,[-1])


    #########带通滤波器##################
    batches=c[0]
    BandpassData=zeros((c[0],c[1]))
    ClutterData=zeros((c[0],c[1]))
    PureData=zeros((c[0],c[1]))
    pnum=76
    firnum=50
    alpha=0.9
    ####################################预处理######################################
    for raw in range(batches):
        for framenum in range(FrameStitchnum):
            blockdata=RawData[raw,(framenum)*pnum+1:min((framenum+1)*pnum,c[1])]
            blockmean=mean(blockdata)
            aa=blockdata.shape

            DCmean=np.ones((1,blockdata.shape[0]))*blockmean
            RawData[raw, (framenum) * pnum + 1:min((framenum + 1) * pnum, c[1])]=blockdata-DCmean

        convres=np.convolve(RawData[raw,:],BanFilter3)

        BandpassData[raw,:]=convres[int(firnum/2):int(firnum/2+c[1])]
        if raw==0:
            ClutterData[raw,:]=(1-alpha)*BandpassData[raw,:]
            PureData[raw,:]=BandpassData[raw,:]-ClutterData[raw,:]
        if raw>0:
            ClutterData[raw,:]=alpha*ClutterData[raw-1,:]+(1-alpha)*BandpassData[raw,:]
            PureData[raw,:]=BandpassData[raw,:]-ClutterData[raw,:]
    PureData=PureData[M:c[0],L:c[1]-50]

    return PureData









