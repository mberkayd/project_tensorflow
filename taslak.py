import os
import subprocess
import numpy as np


"""

"""
#lines = ["LOAD ", "OPER\n", "Visc 1000000\n", "ITER 200\n", "MACH 0.1\n", "PACC\n", "\n","\n","\n","ALFA 0.0","\n","\n","\n","\n","\n","quit"]
lines = ["LOAD ", "PANE\n", "OPER\n", "Visc 1000000\n", "PACC\n", "\n", "\n", "\n","\n","quit"]
path_of_the_directory= 'C:/Users/BerkayD/Desktop/XFOIL/datacsv'

def get_xfoil_results():
    
    for filename in os.listdir(path_of_the_directory):
        lines[0] = "LOAD {path}/{file}\n".format(path = path_of_the_directory,file = filename) 
        lines[5] = "{}_sonuc.txt\n".format(filename.split(".")[0])  
        
        
       
        with open('C:/Users/BerkayD/Desktop/XFOIL/yeniin.txt', 'w') as f:
            f.writelines(lines)
            f.close()
            subprocess.call("xfoil.exe < yeniin.txt", shell=True)


get_xfoil_results()

