#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 11:03:13 2020

@author: joseberrios
"""
import scipy as sp
from scipy.integrate import odeint

# unidades base
cm = 0.01
inch = 2.54*cm
g = 9.81 

# coef de arrastre
p = 1.225
cd = 0.47
D = 8.5*inch
r = D/2
A = sp.pi * r**2
CD= 0.5 * p * cd * A

# masa
m = 15.

# viento
#V = 20.

#funcion a integrar
# z es el vector de estado

# z = [x, y, vx, vy]
# dz/dt = bala(z, t)
#          [   z2    ]
# dz/dt =  [         ]
#          [FD/m  - g]

# vector de estado
# z[0] -> x
# z[1] -> y
# z[2] -> vx
# z[3] -> vy

def bala(z, t, V):
    zp = sp.zeros(4)
    
    zp[0] = z[2]
    zp[1] = z[3]
    v = z[2:4]
    v[0] = v[0] - V
    v2 = sp.dot(v,v)
    vnorm = v2**0.5
    FD = - CD * v2 * (v / vnorm)
    zp[2] = FD[0]/m
    zp[3] = FD[1]/m - g
    
    return zp

# vector de tiempo
t = sp.linspace(0, 30, 1001)
t1 = sp.linspace(0, 30, 100)
# parte en origen y vx = vy

vi = 100*1000./3600
z0 = sp.array([0, 0, vi,vi])

V1 = (0,)
V2 = (10,)
V3 = (20,)

solucion = [odeint(bala, z0, t, V1), odeint(bala, z0, t, V2),
            odeint(bala, z0, t, V3)]


import matplotlib.pylab as plt

x = [solucion[0][:,0], solucion[1][:,0], solucion[2][:,0]]
y = [solucion[0][:,1], solucion[1][:,1], solucion[2][:,1]]

ymax = max(max(y[0]),max(y[1]),max(y[2]))
print (ymax)
xmax = []
for a in range(3):
    print (a)
    for i in range(len(x[0])):
        if y[a][i] < 0:
            xmax.append(x[a][i-1])
            print (i)
            break        
xr = max(xmax)  

plt.figure(dpi=300)
plt.grid()
plt.plot(x[0],y[0], label='V = 0 m/s')
plt.plot(x[1],y[1], label='V = 10 m/s')
plt.plot(x[2],y[2], label='V = 20 m/s')
plt.ylim(bottom = 0, top = ymax*(1.1))
plt.xlim(left = 0, right = xr*1.05)
plt.yticks((0, 10, 20, 30, 40, 50),('0','10','20','30','40','50'))
plt.xlabel('Distancia (m)')
plt.ylabel('Altura (m)')
plt.title('Trayectoria Para Distintos Vientos')
plt.legend()
plt.show()


    
    
    