import os
import subprocess
import numpy as np


"""

"""
#lines = ["LOAD ", "OPER\n", "Visc 1000000\n", "ITER 200\n", "MACH 0.1\n", "PACC\n", "\n","\n","\n","ALFA 0.0","\n","\n","\n","\n","\n","quit"]
#lines = ["LOAD ", "PANE\n", "OPER\n", "Visc 1000000\n", "PACC\n", "\n", "\n", "\n","\n","quit"]
lines = ["LOAD ", "OPER\n", "Visc 1000000\n","ITER 200\n","mach 0.1\n", "PACC\n", "\n", "\n","ALFA 0.0\n","\n","\n","quit"]
path_of_the_directory= 'C:/Users/BerkayD/Desktop/XFOIL'
# load ag03.dat , OPER, 
def get_xfoil_results():
    
    for filename in os.listdir(path_of_the_directory + "/datacsv"):
        lines[0] = "LOAD {path}/datacsv/{file}\n".format(path = path_of_the_directory,file = filename) 
        lines[6] = "{path}/sonuc/{file}_sonuc.txt\n".format(path =path_of_the_directory , file = filename.split(".")[0])  
        
        
       
        with open('C:/Users/BerkayD/Desktop/XFOIL/yeniin.txt', 'w') as f:
            f.writelines(lines)
            f.close()
            subprocess.call("xfoil.exe < yeniin.txt", shell=True)

        cl,cd = compute_coeff(lines[6].split("\n")[0])
        print(cl,cd)

def compute_coeff(sonucdosyasi,reynolds=500000, mach=0, alpha=3, n_iter=200, tmp_dir='tmp' ):
         
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
    




if __name__ == "__main__":
    
    get_xfoil_results()




