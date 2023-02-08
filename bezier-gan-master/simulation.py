#import os
from __future__ import division
import configparser
#import subprocess as sp
import gc
import subprocess
import numpy as np
from scipy.interpolate import interp1d

from utils import safe_remove, create_dir


lines = ["LOAD ", "OPER\n", "Visc 1000000\n","ITER 200\n","mach 0.1\n", "PACC\n", "\n", "\n","ALFA 0.0\n","\n","\n","quit"]
path_of_the_directory= 'C:/Users/BerkayD/Desktop/XFOIL'

def get_xfoil_results(visc=100000, iterr=200, mach=0.1, alfa=0.0):
    lines = ["LOAD ", "OPER\n", "Visc "+str(visc)+"\n","ITER "+str(iterr)+"\n","mach"+str(mach)+"\n", "PACC\n", "\n", "\n","ALFA "+str(alfa)+"\n","\n","\n","quit"]
    for filename in os.listdir(path_of_the_directory + "/datacsv"):
        lines[0] = "LOAD {path}/datacsv/{file}\n".format(path = path_of_the_directory,file = filename) 
        lines[6] = "{path}/sonuc/{file}_sonuc.txt\n".format(path =path_of_the_directory , file = filename.split(".")[0])  
        
        
       
        with open('C:/Users/BerkayD/Desktop/XFOIL/yeniin.txt', 'w') as f:
            f.writelines(lines)
            f.close()
            subprocess.call("xfoil.exe < yeniin.txt", shell=True)

        cl,cd = get_coeff_from_resultfile(lines[6].split("\n")[0])
        print(cl,cd)

def get_coeff_from_resultfile(sonucdosyasi):
         
    cd = np.nan
    cl = np.nan
    with open(sonucdosyasi , 'r') as f:
        count = 0
        Lines = f.readlines()
        for line in Lines:
            if count == 12:
                results = line.split()
                cl = results[1]
                cd = results[2]
                break
            count += 1
            
        
        f.close()
    
    return cl,cd    
    




def main():

    get_xfoil_results()

main()

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
            
#    if np.isnan(perf):
#        from matplotlib import pyplot as plt
#        plt.plot(airfoil[:,0], airfoil[:,1], 'o-', alpha=.5)
#        plt.show()
        
    if return_CL_CD:
        return perf, CL, CD
    else:
        return perf
    
    
if __name__ == "__main__":
    
#    airfoil = np.load('tmp/a18sm.npy')
    airfoils = np.load('data/airfoil_interp.npy')
    airfoil = airfoils[np.random.choice(airfoils.shape[0])]
    
    # Read airfoil operating conditions from a config file
    config_fname = 'op_conditions.ini'
    reynolds, mach, alpha, n_iter = read_config(config_fname)
    
    CL, CD = compute_coeff(airfoil, reynolds, mach, alpha, n_iter)
    print(CL, CD, CL/CD)
