import  numpy as np
import matplotlib.pylab as plt
from pylab import *
mpl.rcParams['font.sans-serif']=['Simhei']#添加字体
x=[0.001,0.003,0.006,0.009,0.01,0.012,0.015,0.018,0.02,0.023,0.025,0.028]
y1=[88.55,89.51,89.86,90.52,91.18,90.70,90.08,89.82,89.73,89.53,89.22,88.76]
#y2=[1,0.3,0.12,0.22,0.33,0.45,2.2]
plt.figure()

plt.plot(x,y1,"k-",marker="o",markersize=2,mec="r",mfc="r",linewidth=1)
#plt.plot(x,y2,"r-.",linewidth=1,label="F1")
plt.xlabel("lr")
plt.ylabel(u"F1值（%）")
plt.title(u"lr对F1值的影响")

plt.grid(which="both",ls=":",linewidth=1)
#plt.legend()
plt.show()