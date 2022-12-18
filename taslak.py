import os
import subprocess
import numpy as np


"""
airfoil_name = "2032"
alpha_i = 0
alpha_f = 10
alpha_step = 0.25
Re = 1000000
n_iter = 100
"""

lines = ["LOAD ", "PANE\n", "OPER\n", "Visc 1000000\n", "PACC\n", "\n", "\n", "\n","\n","quit"]
path_of_the_directory= 'C:/Users/BerkayD/Desktop/XFOIL/datacsv'

for filename in os.listdir(path_of_the_directory):
    f = os.path.join(filename)
    
    print(f)
    lines[0] = "LOAD "
    lines[0] += ("C:/Users/BerkayD/Desktop/XFOIL/datacsv/" +f+ "\n")
    lines[5] = f.split(".")[0] + "_sonuc.txt\n"
        
    with open('C:/Users/BerkayD/Desktop/XFOIL/yeniin.txt', 'w') as f:
        f.writelines(lines)
        f.close()
        subprocess.call("xfoil.exe < yeniin.txt", shell=True)
        


"""
subprocess.call("xfoil.exe < yeniin.txt", shell=True)
"""

"""
for filename in os.listdir(path_of_the_directory):
    lines[0] = "LOAD {}".format(filename) 
    lines[5] = "sonuc_{}".format(filename)

def get_xfoil_results(lines, directory):
    .
    .
    .
    return cl ,cd
 """       

"""komutdosyasi.write("LOAD {0}.dat\n".format(airfoil_name))
komutdosyasi.write(airfoil_name + '\n')
komutdosyasi.write("PANE\n")
komutdosyasi.write("OPER\n")
komutdosyasi.write("Visc {0}\n".format(Re))
komutdosyasi.write("PACC\n")
komutdosyasi.write("sonuc.txt\n\n")
komutdosyasi.write("ITER {0}\n".format(n_iter))
komutdosyasi.write("ASeq {0} {1} {2}\n".format(alpha_i, alpha_f,alpha_step))
"""                                             
"""
komutdosyasi.write("\n\n")
komutdosyasi.write("quit\n")
komutdosyasi.close()
"""

#C:/Users/BerkayD/Desktop/XFOIL/datacsv

