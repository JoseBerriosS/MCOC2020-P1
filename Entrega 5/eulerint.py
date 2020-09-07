#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 15:48:41 2020

@author: joseberrios
"""
from numpy import array, zeros



def eulerint(zp,z0,t, Nsubdivisiones = 1):
    Nt = len(t)
    Ndim = len(array(z0))
    
    z = zeros((Nt,Ndim))
    z[0,:] = z0
    
    for i in range(1,Nt):
        t_anterior = t[i]
        
        dt = (t[i] - t[i-1])/Nsubdivisiones
        
        z[i,:]= z[i-1, :] + dt * zp(z[i-1, :], t_anterior)
        
        z_temp = z[i-1,:].copy()
        for k in range(Nsubdivisiones):
            z_temp += dt * zp(z_temp, t_anterior + k*dt)
            
        z[i, :] = z_temp
        
    return z
