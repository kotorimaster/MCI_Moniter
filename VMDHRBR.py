from VMD_hb import VMD_hb
import numpy as np


def VMDHRBR(HRsignal):
    valueofk = [4,7,10,12,15,20]  # K值有变化，是否固定一个值，只分解一次这样做的原因是小值可能找不到大值可能有不必要的
    # valueofk = [7]
    Y = range(-2 ** 16 // 2, 2 ** 16 // 2 - 1)
    Y = np.array(Y) * 20 / 2 ** 16  # 110HZ[-4, 0, +4] - -[30385, 32769, 35153]    2 - --33961
    flagheart = 0  # 得到结果则置1
    flagbreath=0
    DData = HRsignal
    measuredHeartbeat = -1
    measuredbreath = -1

    for j in range(len(valueofk)):  # 经过几次VMD分解由valueofk中的K值个数来定

        if flagheart == 0 or flagbreath==0:  # 没有找到心率和呼吸则继续增大K进行VMD分解
            K = valueofk[j]
            u = VMD_hb(DData, K)

            fre = np.zeros((K, 2**16))
            provalue = np.zeros((1, K))
            # provalueEnergyRatio = np.zeros((1, K))
            # maxmax = np.zeros((1, K))
            # print(maxmax.shape)

            for i in range(K):
                spectrum = np.fft.fft(u[i, :], 2 ** 16)
                fre[i, :] = np.abs(np.fft.fftshift(spectrum)) * 10000
                # resultvalue = np.max(fre[i, :])
                result = np.argmax(fre[i,:])
                provalue[0,i] = int(np.abs(Y[result]) * 60)  # 存储所有分解出的频率值
                # [resultvalue, result] = max(fre(i, 32769:39323)) # 110Hz只在0--+2Hz之间找
                # provalue(i) = floor(abs(Y(result + 32768)) * 60) # 存储所有分解出的频率值

                # provalueEnergyRatio[0,i] = np.sum(fre[i, 36045:39323] ** 2)  # 1 - 2 / 0 - 4
                # maxmax[0,i] = resultvalue

            if flagheart==0:
                for i in range(K):
                    if 60 < provalue[0,i] < 100:
                        measuredHeartbeat = provalue[0,i]
                        flagheart = 1

            if flagbreath==0:
                for i in range(K):
                    if 10 < provalue[0,i] < 25:
                        measuredbreath = provalue[0,i]
                        flagbreath = 1
        else:
            break

    if (flagheart == 0):
        measuredHeartbeat = -1
    if (flagbreath == 0):
        measuredbreath = -1

    # provalue = []
    return measuredHeartbeat,measuredbreath
