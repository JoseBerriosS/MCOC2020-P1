#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 19:14:10 2020

@author: joseberrios
"""
import math
import numpy as np
import scipy as sp
from scipy.integrate import odeint


# constantes
G = (6.67)*(10**-11)
# masa
mt = (5.972)*(10**24)
om = (7.27)*(10**-5)
J2 = 1.75553e10*1000**5
J3 = -2.619e11*1000**6
mu = 398600.44*1000**3


#funcion a integrar
# z es el vector de estado

# z = [x, y, vx, vy]

# vector de estado
# z[0] -> x
# z[1] -> y
# z[2] -> vx
# z[3] -> vy




def satelite(z,t):
    
    R = np.array([[np.cos(om*t) , -np.sin(om*t), 0], 
                   [np.sin(om*t) , np.cos(om*t), 0 ], 
                   [0               , 0              , 1]])
    R_prima = om*np.array([[-np.sin(om*t), -np.cos(om*t), 0], 
                              [np.cos(om*t) , -np.sin(om*t), 0 ], 
                              [0               , 0               , 0]])
    R_primaprima = (om**2)*np.array([[-np.cos(om*t) , np.sin(om*t), 0], 
                                        [-np.sin(om*t) , -np.cos(om*t), 0 ], 
                                        [0                , 0               , 0]])
            
    
    zp = np.zeros(6)
    
    zp[0] = z[3]
    zp[1] = z[4]
    zp[2] = z[5]
    
    r_3 = (np.sqrt(z[0]**2 + z[1]**2 + z[2]**2))**3 
    
    z1 = z[0:3]
    z2 = z[3:6]
    
    zp[3:6] = -G*mt*z1/(r_3) - R.T @ (2*R_prima @ z2 + R_primaprima @ z1)
    
    return zp 


def satelite_J2(z,t): 
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
    
    
    x = z[0:3]
    xp = z[3:6]
    
    r = (np.dot(x,x)**0.5)
    
    x_arreglo = R@x
    
    rnorma = x_arreglo/r
    
    Fuerza_G = - (mu/r**2) * rnorma
    
    z2 = x_arreglo[2]**2
    
    r_plano = x_arreglo[0]**2 + x_arreglo[1]**2
    
    PJ2 = J2 * x_arreglo / r**7
    
    PJ2[0] = PJ2[0] * (6*z2 - 1.5*r_plano)
    PJ2[1] = PJ2[1] * (6*z2 - 1.5*r_plano)
    PJ2[2] = PJ2[2] * (3*z2 - 4.5*r_plano)
    
    zp[0:3] = xp
    
    zp[3:6] = R.T @ (Fuerza_G + PJ2 - (2*Rp@xp + Rpp@x))

    
    return zp

def satelite_J2J3(z,t): 
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
    
    
    x = z[0:3]
    xp = z[3:6]
    
    r = (np.dot(x,x))**0.5
    
    x_arreglo = R@x
    
    rnorma = x_arreglo/r
    
    Fuerza_G = -(mu/r**2) * rnorma
    
    z2 = x_arreglo[2]**2
    
    r_plano = x_arreglo[0]**2 + x_arreglo[1]**2
    
    PJ2 = J2 * x_arreglo / r**7
    
    PJ2[0] = PJ2[0] * (6*z2 - 1.5*r_plano)
    PJ2[1] = PJ2[1] * (6*z2 - 1.5*r_plano)
    PJ2[2] = PJ2[2] * (3*z2 - 4.5*r_plano)
    
    PJ3 = np.zeros(3)
    PJ3[0] = (J3 * x_arreglo[0]*x_arreglo[2] / r**9) * (10*z2 - 7.5*r_plano)
    PJ3[1] = (J3 * x_arreglo[1]*x_arreglo[2] / r**9) * (10*z2 - 7.5*r_plano)
    PJ3[2] = (J3 / r**9 ) * (4*z2 * (z2 - 3*r_plano) + 1.5*r_plano**2)
    
    
    
    zp[0:3] = xp
    
    zp[3:6] = R.T @ (Fuerza_G + PJ2 + PJ3 - (2*Rp@xp + Rpp@x))

    
    return zp