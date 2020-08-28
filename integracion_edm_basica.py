#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 10:19:33 2020

@author: joseberrios
"""
import scipy as sp
import numpy as np
from scipy.integrate import odeint


# constantes
G = (6.67)*(10**-11)
r = 6371000
d = 700000
# masa
mt = (5.972)*(10**24)
om = (7.27)*(10**-5)

# viento
#V = 20.

#funcion a integrar
# z es el vector de estado

# z = [x, y, vx, vy]

# vector de estado
# z[0] -> x
# z[1] -> y
# z[2] -> vx
# z[3] -> vy


def satelite(z, t):
    zp = np.zeros(6)
    R = np.array([[np.cos(om*t),-np.sin(om*t),0],
                  [np.sin(om*t),np.cos(om*t),0],
                  [0,0,1]])
    
    Rp = om*np.array([[-np.sin(om*t),-np.cos(om*t),0],
                   [np.cos(om*t),-np.sin(om*t),0],
                   [0,0,0]])
    
    Rpp = (om**2)*np.array([[-np.cos(om*t),np.sin(om*t),0],
                    [-np.sin(om*t),-np.cos(om*t),0],
                    [0,0,0]])
    
    
    
    zp[0:3] = z[3:6]
    
    r3 = (r+d)**3
    
    primero = np.dot(((-G*mt)/r3),(z[0:3]))
    
    segundo1 = 2 * np.dot(Rp,z[3:6])
    
    segundo2 = np.dot(Rpp,(z[0:3]))
    
    zp[3:6] = primero + np.dot(-np.transpose(R),(segundo2 + segundo1))

    return zp


# vector de tiempo
hora = 3600
tiempo = hora*8
t = np.linspace(0, tiempo, tiempo +1)



vi = 24000*1000/3600
z0 = np.array([r+d, 0, 0, 0,vi,0])


solucion = odeint(satelite, z0, t)


import matplotlib.pylab as plt

x = solucion[:,0]
y = solucion[:,1]
z = solucion[:,2]

norma = (x**2 + y**2 + z**2)**0.5

plt.figure(dpi=300)


plt.subplot(3,1,1)
plt.title('Historia Tiempo \n x(t)')
plt.ylabel('(km)')
plt.yticks((-10000000,10000000),('-10 km','10 km'))
plt.xticks((0,5000,10000,15000,20000,25000,35000),('','','','','','',''))
plt.ylim(top=10000000, bottom = -10000000)
plt.plot(t,x)
plt.grid()

plt.subplot(3,1,2)
plt.title('y(t)')
plt.ylabel('(km)')
plt.yticks((-10000000,10000000),('-10 km','10 km'))
plt.xticks((0,5000,10000,15000,20000,25000,35000),('','','','','','',''))
plt.ylim(top=10000000, bottom = -10000000)
plt.plot(t,y)
plt.grid()

plt.subplot(3,1,3)
plt.plot(t,z)
plt.ylabel('(km)')
plt.title('z(t)')
plt.xlabel('Tiempo (s)')
plt.yticks((-10000000,10000000),('-10 km','10 km'))
plt.ylim(top=10000000, bottom = -10000000)
plt.tight_layout()
plt.grid()
plt.show()

plt.figure(dpi=300)
plt.plot(t,norma)
plt.xlim(0,tiempo)
plt.grid()
plt.tight_layout()
plt.hlines(r+80000,0,tiempo, color ='green')
plt.ylim(top=7200000)
plt.xlabel('Tiempo (s)')
plt.ylabel('Distancia (km)')
plt.title('Distancia al centro de la tierra del satélite vs. el tiempo')

plt.show()

plt.figure(dpi=300)
num_segmentos = 1000
rad = r+80000
cx = 0
cy = 0

angulo = np.linspace(0, 2*np.pi, num_segmentos+1)
x1 = rad * np.cos(angulo) + cx
y1 = rad * np.sin(angulo) + cy

plt.plot(x1, y1, color='g', label= 'Superficie terrestre')


plt.xlabel('X (km)')
plt.ylabel('Y (km)')
plt.yticks((-r-80000,r+80000),('7 km','7 km'))
plt.xticks((-r-80000,r+80000),('7 km','7 km'))
plt.ylim(top=8000000, bottom = -8000000)
plt.gca().set_aspect('equal')
plt.grid()
plt.plot(x,y, c='lightblue', label='Trayectoria satelite',alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

