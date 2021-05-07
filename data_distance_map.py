import scipy.io as sio
import numpy as np

camera=sio.loadmat('save/1.5m_camera_cwh.mat')['camera']
d=1.5

tmp_camera=[]
for i in range(camera.shape[0]):
    if (camera[i,0]!=0 and camera[i,1]!=0) and (camera[i,3]==0 and camera[i,4]==0):
        tmp_camera.append(camera[i,:])

result=sum(tmp_camera)/len(tmp_camera)
print(result)
print(result[0]*d-(1.75-d)*7,result[1]*d-(1.75-d)*7)

# 1m-->68.57 89.11 6121 -->68.57 89.11 -->63.3 83.9
# 1.5m-->43.82 54.35 2386 -->65.73 81.52 -->63.9 79.8
# 1.5m_cwh -->41.18 50.69 2065 --> 61.76 75.10 -->60 73.4
# 1.5m_zxy -->38.79 48.51 1884 --> 58.17 72.76 -->56.4 71
# 2m-->30.93 38.32 1187 -->61.87 76.64 -->63.6 78.4
# 2.5m-->25.30 30.88 7828 -->63.25 77.20

#列加15 前后30

