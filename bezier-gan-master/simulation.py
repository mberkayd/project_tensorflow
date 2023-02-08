import os
import configparser
import pexpect
import subprocess
import gc
import numpy as np
from scipy.interpolate import interp1d




def compute_coeff(reynolds=10000 ,n_iter=200 ,mach=0.1 ,alpha=0.0, temp=[]):
    
    path = r"C:\Users\PC\Desktop\TENSORFLOW\deney\airfoils"

    for dir_list in os.listdir(path):
        if  dir_list[len(dir_list)-3:]=="csv" or dir_list[len(dir_list)-3:]=="dat":
           temp.append(dir_list)
    x=0
    CL=[]
    CD=[]

    while x<len(temp):
       
       airfoil=(temp[x])
       
       y=os.path.splitext(airfoil)
       airfoil2= (y[0])
       
       
       with open("input.txt", "w") as inputx:
                inputx.write("LOAD " + airfoil + "\n"+ airfoil +"\n"+"OPER\n" + "VISC"+ str(reynolds)+ "\n" + "ITER"+ str(n_iter) + "\n" + "MACH"+ str(mach) + "\n" + "PACC\n"+airfoil2+".log\n"+"\n"+"ALFA"+str(alpha)+"\n"+"\n"+"quit")
                
       subprocess.call("xfoil.exe < input.txt", shell=True) 
       airfoillog=airfoil2+".log"

       values= open(airfoillog,"r") 
       content=values.readlines()
       line=content[12]
       line=line.split()

       cl= float(line[1])
       cd= float(line[2])
       
       
       CL.append(cl)
       CD.append(cd)    
    
       x=x+1
    
    return CL, CD

def read_config(config_fname):
    
    # Airfoil operating conditions
    Config = configparser.ConfigParser()
    Config.read(config_fname)
    reynolds = float(Config.get('OperatingConditions', 'Reynolds'))
    mach = float(Config.get('OperatingConditions', 'Mach'))
    alpha = float(Config.get('OperatingConditions', 'Alpha'))
    n_iter = int(Config.get('OperatingConditions', 'N_iter'))
    
    return reynolds, mach, alpha, n_iter

def detect_intersect(airfoil):
    # Get leading head
    lh_idx = np.argmin(airfoil[:,0])
    lh_x = airfoil[lh_idx, 0]
    # Get trailing head
    th_x = np.minimum(airfoil[0,0], airfoil[-1,0])
    # Interpolate
    f_up = interp1d(airfoil[:lh_idx+1,0], airfoil[:lh_idx+1,1])
    f_low = interp1d(airfoil[lh_idx:,0], airfoil[lh_idx:,1])
    xx = np.linspace(lh_x, th_x, num=1000)
    yy_up = f_up(xx)
    yy_low = f_low(xx)
    # Check if intersect or not
    if np.any(yy_up < yy_low):
        return True
    else:
        return False

def evaluate(airfoil, config_fname='op_conditions.ini', return_CL_CD=False):
    
    # Read airfoil operating conditions from a config file
    reynolds, mach, alpha, n_iter = read_config(config_fname)
    
    if detect_intersect(airfoil):
        print('Unsuccessful: Self-intersecting!')
        perf = np.nan
        CL = np.nan
        CD = np.nan
    
    elif np.abs(airfoil[0,0]-airfoil[-1,0]) > 0.01 or np.abs(airfoil[0,1]-airfoil[-1,1]) > 0.01:
        print('Unsuccessful:', (airfoil[0,0],airfoil[-1,0]), (airfoil[0,1],airfoil[-1,1]))
        perf = np.nan
        CL = np.nan
        CD = np.nan
        
    else:
        
        CL, CD = compute_coeff(airfoil, reynolds, mach, alpha, n_iter)
        perf = CL/CD
        
        if perf < -100 or perf > 300 or CD < 1e-3:
            print('Unsuccessful:', CL, CD, perf)
            perf = np.nan
        elif not np.isnan(perf):
            print('Successful: CL/CD={:.4f}'.format(perf))
            

        
    if return_CL_CD:
        return perf, CL, CD
    else:
        return perf
    
    
if __name__ == "__main__":
    

    airfoils = np.load('data/airfoil_interp.npy')
    airfoil = airfoils[np.random.choice(airfoils.shape[0])]
    
    # Read airfoil operating conditions from a config file
    config_fname = 'op_conditions.ini'
    reynolds, mach, alpha, n_iter = read_config(config_fname)
    
    CL, CD = compute_coeff(reynolds, mach, alpha, n_iter)
    
    print(CL, CD, CL/CD)