# coding=gbk
import wave
import matplotlib.pyplot as plt
import numpy as np
import os

print(wave.__file__)

filepath="E:\\z.wav"
f = wave.open(filepath,'rb')
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
strData = f.readframes(nframes)#��ȡ��Ƶ���ַ�����ʽ
waveData = np.fromstring(strData,dtype=np.int16)#���ַ���ת��Ϊint
waveData = waveData*1.0/(max(abs(waveData)))#wave��ֵ��һ��
# plot the wave
time = np.arange(0,nframes)*(1.0 / framerate)
f.close()
plt.plot(time,waveData)
plt.xlabel("Time(s)")
plt.ylabel("Amplitude")
plt.title("Single channel wavedata")
plt.grid('on')#��ߣ�on���У�off:�ޡ�

plt.legend()

plt.show()