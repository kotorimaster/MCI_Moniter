from numpy import *
import numpy as np
def lse(AP,centroids,n):
    m=centroids.shape[0]

    RN_n=AP.shape[0]#3
    x=AP[:,0]#1,3
    y=AP[:,1]
    x=np.reshape(x,[1,-1])
    y = np.reshape(y, [1, -1])
    rxx=zeros((m,1),dtype=float32)
    ryy=zeros((m,1),dtype=float32)
    for j in range(m):
        A=zeros((RN_n,2))
        b=zeros((RN_n,1))
        r=centroids[j,:]
        r=np.reshape(r,[1,-1])
        for q in range(RN_n):

            A[q,0]=-2*(x[0,q]-x[0,RN_n-1])
            A[q, 1] = -2 * (y[0, q] - y[0, RN_n-1])
        for p in range(n):
            for qq in range(RN_n):
                b[qq,0]=r[0,qq]*r[0,qq]-r[0,RN_n-1]*r[0,RN_n-1]-x[0,qq]*x[0,qq]+x[0,RN_n-1]*x[0,RN_n-1]-y[0,qq]*y[0,qq]+y[0,RN_n-1]*y[0,RN_n-1]


            xls2=np.dot(np.dot(np.linalg.pinv(np.dot(transpose(A),A)),transpose(A)),b)
        rxx[j]=xls2[0]
        ryy[j]=xls2[1]


    return rxx,ryy

