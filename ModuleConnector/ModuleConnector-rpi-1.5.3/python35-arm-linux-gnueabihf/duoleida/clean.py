import numpy as np


# [cmap, dmap, n, ht] = clean(input_signal, template_signal, Tclean)
# clean算法
# input_signal为一行输入信号，template_signal为模板信号
# Tclean为阈值
# ht为clean算法解卷积后的相应函数
def clean(input_signal, template_signal, Tclean):
    dmap = input_signal  # dirty map
    length = len(input_signal)  # 输入信号长度
    cmap = np.zeros(length)  # clean map
    n = 0  # iteration counter
    tl = template_signal.shape[1]  # 模板信号长度
    tsignal = np.zeros(length)  # 模板信号补零，使其长度与输入信号相等
    tsignal[0: tl] = template_signal
    ht = np.zeros(length)  # clean算法解卷积后的相应函数

    Rxx = np.correlate(tsignal, tsignal)  # 模板信号自相关
    R0 = Rxx

    # print(np.correlate(dmap, dmap))
    Rxy = np.correlate(dmap, tsignal, 'full')  # 互相关
    Rl = len(Rxy)
    R = Rxy[Rl//2:] / R0  # 归一化

    Rmax = max(R)
    loc = np.argmax(R)
    # print(loc)
    # Tclean = Tclean * Rmax
    while Rmax > Tclean:
        maxloc = loc  # 互相关最大时对应的时移
        # if maxloc < 0:
        #     print('maxloc<0')
        #     maxloc = -maxloc
        # print(maxloc)
        # print('----'+str(n)+'----')[]
        ht[maxloc] = 1
        stsignal = np.zeros(length)  # 时移后的模板信号
        if maxloc + tl < length:
            stsignal[maxloc: maxloc + tl] = template_signal
        else:
            stsignal[maxloc:] = template_signal[0,0:(length - maxloc)]

        newmap = Rmax * stsignal
        dmap = dmap - newmap
        cmap = cmap + newmap
        n = n + 1
        Rxy = np.correlate(dmap, tsignal, 'full')
        Rl = len(Rxy)
        R = Rxy[Rl // 2:] / R0  # 归一化
        Rmax = max(R)
        # print(str(Rmax)+'  '+str(R0))
        loc = np.argmax(R)
    return cmap, dmap, n, ht
