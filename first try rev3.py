def perf_deg(path=r"C:\Users\PC\Desktop\TENSORFLOW\deney\airfoils"):
    
import subprocess
import os

temp=[]
path = r"C:\Users\PC\Desktop\TENSORFLOW\deney\airfoils"

for dir_list in os.listdir(path):
    if  dir_list[len(dir_list)-3:]=="csv" or dir_list[len(dir_list)-3:]=="dat":
        temp.append(dir_list)    

x=0
while x<len(temp):
    airfoil=(temp[x]) 
    y=os.path.splitext(airfoil)
    airfoil2= (y[0])
    
    with open("input.txt", "w") as input:
             input.write("LOAD " + airfoil + "\n"+ airfoil +"\n"+"OPER\n" + "VISC 10000.0\n" + "ITER 200\n" + "MACH 0.1\n" + "PACC\n"+airfoil2+".log\n"+"\n"+"ALFA 0.0\n"+"\n"+"quit")
             
    subprocess.call("xfoil.exe < input.txt", shell=True) 
    airfoillog=airfoil2+".log"

    values= open(airfoillog,"r")
    content=values.readlines()
    line=content[12]
    line=line.split()

    cl= float(line[1])
    cd= float(line[2])
    
    print (airfoil2,"airfoili için,")
    print ("CL=",cl,"  CD=",cd)
    print("Performans değeri=",cl/cd)
    print()
   
    x=x+1  
