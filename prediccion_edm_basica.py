#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:10:46 2020

@author: joseberrios
"""
import numpy as np
from scipy.integrate import odeint
import datetime as dt
from matplotlib.pylab import *
# Vector de estado inicial:
    
#<TAI>TAI=2020-08-05T23:00:19.000000</TAI>
#<UTC>UTC=2020-08-05T22:59:42.000000</UTC>
#<UT1>UT1=2020-08-05T22:59:41.796108</UT1>
#<Absolute_Orbit>+22794</Absolute_Orbit>
#<X unit="m">-682968.916400</X>
#<Y unit="m">5153970.686656</Y>
#<Z unit="m">-4807588.442651</Z>
#<VX unit="m/s">2471.956223</VX>
#<VY unit="m/s">-4707.396469</VY>
#<VZ unit="m/s">-5402.677076</VZ>
#<Quality>NOMINAL</Quality>

# Vector de estado final:

#<TAI>TAI=2020-08-07T01:00:19.000000</TAI>
#<UTC>UTC=2020-08-07T00:59:42.000000</UTC>
#<UT1>UT1=2020-08-07T00:59:41.796594</UT1>
#<Absolute_Orbit>+22810</Absolute_Orbit>
#<X unit="m">1102835.919384</X>
#<Y unit="m">6094382.559245</Y>
#<Z unit="m">3414273.664709</Z>
#<VX unit="m/s">2283.248247</VX>
#<VY unit="m/s">3231.588637</VY>
#<VZ unit="m/s">-6483.825930</VZ>
#<Quality>NOMINAL</Quality>


utc_EOF_format =           "%Y-%m-%dT%H:%M:%S.%f"
t1= dt.datetime.strptime("2020-08-05T22:59:42.000000",utc_EOF_format)
t2= dt.datetime.strptime("2020-08-07T00:59:42.000000",utc_EOF_format)

intervalo = t2 - t1
intervalo_en_segundos = intervalo.total_seconds()

G = (6.67e-11)      # Nm/kg**2
r = (6371000)        # m
mt = (5.972e24)     # kg
om = (7.27e-5)      # rad/s

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
    
    r3 = (np.dot(z[0:3],z[0:3])**0.5)**3
    
    primero = np.dot(((-G*mt)/r3),(z[0:3]))
    
    segundo1 = 2 * np.dot(Rp,z[3:6])
    
    segundo2 = np.dot(Rpp,(z[0:3]))
    
    zp[3:6] = primero + np.dot(-np.transpose(R),(segundo2 + segundo1))

    return zp


t = np.linspace(0, 93600, 93600 +1)

# z = [x, y, z, vx, vy, vz]   z[0:3]= m   z[3:6]= m/s

z0 = np.array([-682968.916400, 5153970.686656, -4807588.442651,
               2471.956223,-4707.396469,-5402.677076])

zf = np.array([1102835.919384, 6094382.559245, 3414273.664709,
               2283.248247,3231.588637,-6483.825930])

solucion = odeint(satelite, z0, t)

ultima_pos = solucion[:,:][-1]

deriva = ultima_pos[0:3] - zf[0:3]

imprimir = np.dot(deriva,deriva)**0.5

print (f'Diferencia entre la prediccion y la posicion exacta: {imprimir} m')





