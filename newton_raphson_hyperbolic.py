import pandas as pd
import math as math
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d



df=pd.read_csv("C:/Users/yashu/Desktop/python/Reservoir/NorneProdData.csv")
q_arr=[]
t_arr=[]

for i in range(len(df)):
    q_arr.append(df.iloc[i,1])
    t_arr.append(df.iloc[i,0])

q_t_avg=round(math.sqrt(q_arr[0]*q_arr[-1]),3)
f=interp1d(q_arr,t_arr,kind='cubic')
t_avg=f(q_t_avg)
# plt.plot(q_arr,t_arr)
# plt.xlabel('flow rate')
# plt.ylabel('time')
# plt.show()
i=0
b=0.5
b_arr=[]
b_arr.append(0)
b_arr.append(b)
while (b_arr[i+1]-b_arr[i])>0.000001:

    

    func_b=(t_avg*math.pow((q_arr[0]/q_arr[-1]),b))-(t_arr[-1]*math.pow((q_arr[0]/q_t_avg),b))+(t_arr[-1]-t_avg)
    func_b_derv=(t_avg*math.pow((q_arr[0]/q_arr[-1]),b)*math.log(q_arr[0]/q_arr[-1]))-(t_arr[-1]*math.pow((q_arr[0]/q_t_avg),b)*math.log(q_arr[0]/q_t_avg))

    b=b-(func_b/func_b_derv)
    b_arr.append(b)

    i=i+1

# print(b_arr)
Di=((math.pow(q_arr[0]/q_arr[-1],b_arr[-1]))-1)/(b_arr[-1]*t_arr[-1])
D_exp=(math.log(q_arr[0]/q_arr[-1]))/t_arr[-1]
q_arr_exp=[]
q_arr_new=[]
for i in range(len(t_arr)):
    q=q_arr[0]/(math.pow(1+(b_arr[-1]*Di*t_arr[i]),(1/b_arr[-1])))
    q_arr_new.append(q)
    q1=q_arr[0]*math.exp((-D_exp*t_arr[i]))
    q_arr_exp.append(q1)

plt.plot(t_arr,q_arr,label='Original',color='blue')
plt.plot(t_arr,q_arr_new,label='Fit',color='orange')
plt.plot(t_arr,q_arr_exp,label='Exponential fit',color='green')
plt.xlabel("Time")
plt.ylabel("Flow Rate")
plt.legend()
plt.show()




