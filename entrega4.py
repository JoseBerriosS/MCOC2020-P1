#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 16:26:04 2020

@author: joseberrios
"""
from matplotlib.pylab import *
from scipy.integrate import odeint
import numpy as np
from numpy import *
from eulerint import eulerint

#datos

m = 1. #kg
f = 1. #Hz
xi = 0.2
w = 2.*pi*f
k = m*(w**2.)
c = 2*xi*w*m


# ecuacion:
# m*xpp + c*xp + kx=0

#z = [x,vx]  z[0] = m  z[1] = m/s

# se define la funcion z punto para poder resolver ecuacion

def zp(z,t):
    
    x = z[0]
    xp = z[1]
    
    zp = zeros(2)
    zp[0] = xp
    zp[1] = (-k*x-c*xp)/m
    
    return zp

# vector tiempo

t = linspace(0, 4.,1000)

# condicion inicial

z0 = [1.,1.]

# solucion odeint

sol = odeint(zp, z0, t)
z_odeint = sol[:,0]

# solucion analitica

primer_termino = e**(-xi*w*t)
segundo_termino = m*cos(w*((1-xi**2)**0.5)*t)
tercer_termino = ((1+w*xi*m)/(w*((1-xi**2)**0.5)))*sin(w*((1-xi**2)**0.5)*t)

z_real = primer_termino*(segundo_termino + tercer_termino)


#las soluciones para eulerint

sol1 = eulerint(zp, z0, t, Nsubdivisiones = 1 )
z_euler1 = sol1[:,0]

sol10 = eulerint(zp, z0, t, Nsubdivisiones = 10 )
z_euler10 = sol10[:,0]

sol100 = eulerint(zp, z0, t, Nsubdivisiones = 100 )
z_euler100 = sol100[:,0]


# ploteo de las soluciones

figure(dpi=300)
plot(t,z_odeint, c ='dodgerblue', label='odeint')

plot(t,z_real, '-k', linewidth=2 , label='analitica')

plot(t,z_euler1, '--', c='limegreen', label='eulerint Nsubdivisiones = 1', alpha=0.6)

plot(t,z_euler10, '--', c='red', label='eulerint Nsubdivisiones = 10', alpha=0.4)

plot(t,z_euler100, '--', c='orange', label='eulerint Nsubdivisiones = 100', alpha=0.7)

title('Oscilador Armonico')
ylabel('x(t)')
xlabel('tiempo en segundos')
grid()
xlim(left=0)
tight_layout()
legend()

show()
 


