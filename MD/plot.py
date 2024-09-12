import numpy as np
import matplotlib.pyplot as plt
import os

def extract_lattice_data(logfile):
    _step = []
    _Lx = []
    _Ly = []
    _Lz = []
    
    with open(logfile, 'r') as f:
        status = False
        lines = f.readlines()
        for line in lines:
            if "Step          Temp" in line:
                status = True
                continue

            if status:    
                if "WARNING:" in line:
                    continue
                elif "Loop time" in line:
                    break
                else:
                    data = line.split()
                    if len(data) < 10:
                        continue 
                    step = int(data[0])
                    Lx = float(data[7]) / 4  
                    Ly = float(data[8]) / 4
                    Lz = float(data[9]) / 4
                    _step.append(step)
                    _Lx.append(Lx)
                    _Ly.append(Ly)
                    _Lz.append(Lz)

    data = np.column_stack((_step, _Lx, _Ly, _Lz))
    np.savetxt('lattice.txt', data, header='Step Lx Ly Lz', fmt='%d %f %f %f')


def process_lattice_data():
    temperatures = [300, 450, 600, 750, 900]
    lat_data = []

    for temp in temperatures:
        os.chdir(str(temp))  
        extract_lattice_data('log.lammps')  
        data = np.loadtxt('lattice.txt', skiprows=1)  
        nlines = data.shape[0]
        start_line = int(nlines / 3 + 0.5)
        
        selected_data = data[start_line:, 1:4]  
        Lx_avg = np.mean(selected_data[:, 0])
        Ly_avg = np.mean(selected_data[:, 1])
        Lz_avg = np.mean(selected_data[:, 2])
        
        lat_data.append([temp, Lx_avg, Ly_avg, Lz_avg])
        os.chdir('..') 

    lat_data = np.array(lat_data)
    np.savetxt('lat.dat', lat_data, fmt='%d %f %f %f')

def sort_and_plot():
    data = np.loadtxt('lat.dat')
    
    sorted_data = []
    for row in data:
        temp = row[0]
        a, b, c = sorted(row[1:4])
        sorted_data.append([temp, a, b, c])
    
    sorted_data = np.array(sorted_data)
    
    np.savetxt('sorted_lat.dat', sorted_data, fmt='%d %f %f %f')

    plt.figure()
    plt.plot(sorted_data[:, 0], sorted_data[:, 1], marker='s', linestyle='-', label='a')
    plt.plot(sorted_data[:, 0], sorted_data[:, 2], marker='s', linestyle='-', label='b')
    plt.plot(sorted_data[:, 0], sorted_data[:, 3], marker='s', linestyle='-', label='c')
    
    plt.xlabel('Temperature (K)')
    plt.ylabel('Lattice parameter (Å)')
    plt.legend()
    plt.grid(True)
    plt.savefig('lattice_parameters_vs_temperature.png')
    plt.show()

process_lattice_data() 
sort_and_plot() 

