import os
import subprocess
import numpy as np




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


