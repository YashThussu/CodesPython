import matplotlib.pyplot as plt
import math as math
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import seaborn as sns
sns.set()

class Decline_Curves:
    def input_data(self): 
        """returns three output values in order time [array], flow rate[array], Type of Decline (string)"""
        opt=int(input("Enter the type of Decline \n1.Exponential \n2.Hyperbolic \n3.Harmonic \n"))      
        qi=float(input('Enter the inital flow rate:\n'))
        t=int(input('Enter the time in months:\n'))
        tf=list(range(t+1))
        Di=float(input("Enter the decline rate:\n"))
        qt=[]
        if opt==1:
            #Exponential Decline b=0
            t1="Exponetial Decline Curve"
            for i in range(len(tf)):
                cal=round(qi*math.pow(math.e,(-1*tf[i]*Di)),3)
                qt.append(cal)
        elif opt==2:
            #Hyberbolic Decline
            t1="Hyperbolic Decline Curve"
            b=float(input('enter the value of b:\n'))
            if (b<1.000) & (b>0.000):
                for i in range(len(tf)):
                    cal=round(qi/(math.pow((1+(b*Di*tf[i])),(1/b))),3)
                    qt.append(cal)
            else:
                print("Select appropriate value of b:")
        else:
            #Harmonic decline  b=1
            t1="Harmonic Decline Curve"
            for i in range(len(tf)):
                cal=round(qi/(1+(Di*tf[i])),3)
                qt.append(cal)

        return tf,qt,t1
        # return (p1+p2)


    def plot_curves(self,a,b,c):
        plt.plot(a,b)
        plt.xlabel("Time")
        plt.ylabel("Flow rate")
        plt.title(c)
        plt.show()
    
    
class Decline_Curves_fit():

    def path(self):
        loc=input("Enter the path of the file:")
        loc=loc.replace("\\","/")
        
        if 'csv' in loc:
            
            return loc

        else:
            return "File not csv" 

        

    def input_data(self,location):
        """input a data from a csv file with first column as time and second column as flow rate"""
        df=pd.read_csv(location)
        t_arr=[]
        flow_arr=[]
        for i in range(len(df)):
            t_arr.append(df.iloc[i,0])
            flow_arr.append(df.iloc[i,1])
        
        return t_arr,flow_arr
    
    def fit_curve(self):

        """fits the curve to the data points and returns fitted flow rate,optimised paramters (initial flow rate, Decline rate, b-exponent,
            flow rate, time as arrays"""
        t=[]
        q=[]
        t,q=self.input_data(location=self.path())
        time_arr=np.array(t)
        flow_arr=np.array(q)
        time_arr1=time_arr/max(time_arr)
        flow_arr1=flow_arr/max(flow_arr)
    
        def arps_eqn(t,qi,Di,b):

            return (qi/(np.abs(1+(b*Di*t))**(1/b)))
        
        popt,pcov=curve_fit(arps_eqn,time_arr1,flow_arr1)


        def arps_eqn_denormal():

            return (popt[0]*max(flow_arr))/((1+(popt[2]*popt[1]*time_arr1))**(1/popt[2]))

        flow_fitted=arps_eqn_denormal()

        return flow_fitted,popt,flow_arr,time_arr

    def Cumulative_production(self,b_exp,q_initial,Decline_rate,q_arr):
        """Calculates Cumulative production of the decline curves, takes 6 input parameters b exponent, decline rate, q intial ,q final and q1 if given"""

        # qt1=q_initial/(math.pow(1+(b_exp*Decline_rate*t1),b_exp))
        # qt2=q_initial/(math.pow(1+(b_exp*Decline_rate*t2),b_exp))
        Gpt=(math.pow(q_initial,b_exp)*(math.pow(q_initial,1-b_exp)-np.power(q_arr,1-b_exp)))/(Decline_rate*(1-b_exp))
        return Gpt

    
    def plot(self):

        """plots two curves one a fitted curve and other cumulative production curve"""

        arr1,arr2,arr3,arr4=self.fit_curve()
        value1=arr2[0]*max(arr3)
        value2=(arr2[1]/max(arr4))
        arr5=self.Cumulative_production(arr2[2],value1,value2,arr1)

        #plot 1
        plt.subplot(2,1,1)
        plt.plot(arr4,arr3,label='Actual Curve')
        plt.plot(arr4,arr1,'--',label=f'b={round(arr2[2],3)}, Di={round(arr2[1]/max(arr4),3)}')
        plt.ylabel('Flow rate')
        plt.xlabel('Days')
        plt.legend()
        
        
        #plot 2
        plt.subplot(2,1,2)
        plt.plot(arr4,arr5,label='Cumulative production vs Time')
        plt.xlabel('Days')
        plt.ylabel('Cumulative Production')
        plt.legend()
        plt.legend()
        plt.show()

        






