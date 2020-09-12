#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 00:43:36 2020

@author: joseberrios
"""

from sys import argv
from scipy.integrate import odeint
import numpy as np
from numpy import *
import xml
import xml.etree.ElementTree as ET
from numpy import zeros
from datetime import datetime, timedelta
import datetime as dt


km = 1000
G = 6.674e-11           
M = 5.972e24            
w = 7.2920150e-5    
J2 = (1.7555e10)*(km**5)
J3 = -(2.61913e11)*(km**6)
Rt = 6378e3
mu = 398600.44*(km**3)

Nt = 8

C = np.zeros((Nt+1,Nt+1))
S = np.zeros((Nt+1,Nt+1)) 

C[4,0], S[4,0] =    0.16193312050719E-05   ,     0.0
C[5,0], S[5,0] =    0.22771610163688E-06   ,     0.0

J4 = C[4,0]/((Rt**4)*mu)
J5 = C[5,0]/((Rt**5)*mu)



def satelite_J2J3(z,t):
    
    theta = (w*t)
    R   = np.array([[np.cos(theta), -np.sin(theta), 0],
                    [np.sin(theta), np.cos(theta), 0],
                    [0, 0, 1]])
    
    Rp = np.array([[-np.sin(theta), -np.cos(theta), 0],
                      [np.cos(theta), -np.sin(theta), 0],
                      [0, 0, 0]])
    
    Rpp =    np.array([[-np.cos(theta), np.sin(theta), 0],
                      [-np.sin(theta), -np.cos(theta), 0],
                      [0, 0, 0]])

    x = z[0:3]
    xp = z[3:6]
    
    r = np.sqrt(np.dot(x,x))
    
    xstill = R@x
    rnorm = (xstill)/(r)
    
    FG = -((398600.440*(km**3))/(r**2))*rnorm
    z2 = (xstill[2])**2
    rflat = ((xstill[0])**2) + ((xstill[1])**2)
    rp = xstill[0]**2 + xstill[1]**2
    rp2 = xstill[0]**2 + xstill[1]**2 + xstill[2]**2 
    
    FJ2= (J2*xstill)/(r**7)
    FJ2[0] = (FJ2[0])*((6*z2) - (1.5*rflat))
    FJ2[1] = (FJ2[1])*((6*z2) - (1.5*rflat))
    FJ2[2] = (FJ2[2])*((3*z2) - (4.5*rflat))


    FJ3 = zeros(3)
    FJ3[0] = ((J3*xstill[0]*xstill[2]) / (r**9)) * (10*z2 - 7.5*rflat)
    FJ3[1] = ((J3*xstill[1]*xstill[2]) / (r**9)) * (10*z2 - 7.5*rflat)
    FJ3[2] = ((J3)                     / (r**9)) * ( (4*z2*(z2 - 3*rflat)) + (1.5*(rflat**2)))
    
    FJ4 = np.zeros(3)
    FJ4[0] = -5*xstill[0]*(35*z2**2/((8*rp**2)**2) - 15*xstill[2]**2/(4*(rp2)) + 0.375)/(rp2)**(7/2) + (-35*xstill[0]*xstill[2]**4/(2*(rp2)**3) + 15*xstill[0]*xstill[2]**2/(2*(rp2)**2))/(rp2)**(5/2)
    FJ4[1] = -5*xstill[1]*(35*z2**2/((8*rp**2)**2) - 15*xstill[2]**2/(4*(rp2)) + 0.375)/(rp2)**(7/2) + (-35*xstill[1]*xstill[2]**4/(2*(rp2)**3) + 15*xstill[1]*xstill[2]**2/(2*(rp2)**2))/(rp2)**(5/2) 
    FJ4[2] = -5*xstill[2]*(35*z2**2/((8*rp**2)**2) - 15*xstill[2]**2/(4*(rp2)) + 0.375)/(rp2)**(7/2) + (-35*xstill[2]**5/(2*(rp2)**3) + 25*xstill[2]**3/((rp2)**2) - 15*xstill[2]/(2*rp2))/(rp2)**(5/2)
    
    FJn4 = FJ4*J4 
    
    FJ5 = np.zeros(3)
    FJ5[0] = -6*xstill[0]*(63*xstill[2]**5/(8*(rp2)**(5/2)) - 35*xstill[2]**3/(4*(xstill[0]**2 + xstill[1]**2 + xstill[2]**2)**(3/2)) + 15*xstill[2]/(8*sqrt(rp2)))/(xstill[0]**2 + xstill[1]**2 + xstill[2]**2)**4 + (-315*xstill[0]*xstill[2]**5/(8*(rp2)**(7/2)) + 105*xstill[0]*xstill[2]**3/(4*(rp2)**(5/2)) - 15*xstill[0]*xstill[2]/(8*(rp2)**(3/2)))/(rp2)**3
    FJ5[1] = -6*xstill[1]*(63*xstill[2]**5/(8*(rp2)**(5/2)) - 35*xstill[2]**3/(4*(xstill[0]**2 + xstill[1]**2 + xstill[2]**2)**(3/2)) + 15*xstill[2]/(8*sqrt(rp2)))/(xstill[0]**2 + xstill[1]**2 + xstill[2]**2)**4 + (-315*xstill[1]*xstill[2]**5/(8*(rp2)**(7/2)) + 105*xstill[1]*xstill[2]**3/(4*(rp2)**(5/2)) - 15*xstill[1]*xstill[2]/(8*(rp2)**(3/2)))/(rp2)**3
    FJ5[2] = -6*xstill[2]*(63*xstill[2]**5/(8*(rp2)**(5/2)) - 35*xstill[2]**3/(4*(xstill[0]**2 + xstill[1]**2 + xstill[2]**2)**(3/2)) + 15*xstill[2]/(8*sqrt(rp2)))/(xstill[0]**2 + xstill[1]**2 + xstill[2]**2)**4 + (-315*xstill[2]**6/(8*(rp2)**(7/2)) + 525*xstill[2]**4/(8*(rp2)**(5/2)) - 225*xstill[2]**2/(8*(rp2)**(3/2)) + 15/(8*sqrt(rp2)))/(rp2)**3
  
    FJn5 = FJ5*J5
  
    
    zp = zeros(6)
    zp[0:3] = xp
    zp[3:6] = R.T@(FG + FJ2 + FJ3 + FJn4 + FJn5- ( ((2*w*Rp)@(xp)) + (((w**2)*Rpp)@(x))) )
    return zp   
     


def utc2time(utc, ut1, EOF_datetime_format = "%Y-%m-%dT%H:%M:%S.%f"):
	t1 = dt.datetime.strptime(ut1,EOF_datetime_format)
	t2 = dt.datetime.strptime(utc,EOF_datetime_format)
	return (t2 - t1).total_seconds()


def leer_eof(fname):
	tree = ET.parse(fname)
	root = tree.getroot()

	Data_Block = root.find("Data_Block")		
	List_of_OSVs = Data_Block.find("List_of_OSVs")

	count = int(List_of_OSVs.attrib["count"])
    
	t = zeros(count)
	x = zeros(count)
	y = zeros(count)
	z = zeros(count)
	vx = zeros(count)
	vy = zeros(count)
	vz = zeros(count)
	u = []
	for i in range(count):
		u.append([])
    
	set_ut1 = False
	for i, osv in enumerate(List_of_OSVs):
		UTC = osv.find("UTC").text[4:]
		u[i] = osv.find("UTC").text[4:]
		x[i] = osv.find("X").text   #conversion de string a double es implicita
		y[i] = osv.find("Y").text
		z[i] = osv.find("Z").text
		vx[i] = osv.find("VX").text
		vy[i] = osv.find("VY").text
		vz[i] = osv.find("VZ").text

		if not set_ut1:
			ut1 = UTC
			set_ut1 = True

		t[i] = utc2time(UTC, ut1)

	return t, x, y, z, vx, vy, vz, u



nombre_eof = argv[1]
#nombre_eof = 'S1B_OPER_AUX_POEORB_OPOD_20200826T111204_V20200805T225942_20200807T005942.EOF'
t, x, y, z, vx, vy, vz , u =  leer_eof(nombre_eof)

eof_out = nombre_eof.replace('.EOF', '.PRED')


z0 = [x[0],y[0],z[0],vx[0],vy[0],vz[0]]

solucion = odeint(satelite_J2J3,z0, t)

sat_x = solucion[:,0]
sat_y = solucion[:,1]
sat_z = solucion[:,2]
sat_vx = solucion[:,3]
sat_vy = solucion[:,4]
sat_vz = solucion[:,5]

EOF_datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
UTC1 = dt.datetime.strptime(u[0],EOF_datetime_format)

with open(eof_out,"w") as fout:
    Nt = len(t)
    fout.write("<Data_Block type=\"xml\">\n  <List_of_OSVs count=\"9361\">\n")
    for i in range(Nt):
        obj = UTC1
        fecha = (obj + timedelta(seconds=t[i])).strftime("%Y-%m-%dT%H:%M:%S.%f")
        fout.write(f"    <OSV>\n      <UTC>UTC={fecha}</UTC>\n      <X unit=\"m\">{sat_x[i]}</X>\n      <Y unit=\"m\">{sat_y[i]}</Y>\n      <Z unit=\"m\">{sat_z[i]}</Z>\n      <VX unit=\"m/s\">{sat_vx[i]}</VX>\n      <VY unit=\"m/s\">{sat_vy[i]}</VY>\n      <VZ unit=\"m/s\">{sat_vz[i]}</VZ>\n      <Quality>NOMINAL</Quality>\n    </OSV>\n")
    fout.write("  </List_of_OSVs>\n</Data_Block>\n</Earth_Explorer_File>")
    
delta = ((sat_x-x)**2 + (sat_y-y)**2 + (sat_z-z)**2 + (sat_vx-vx)**2 + (sat_vy-vy)**2 + (sat_vz-vz)**2)**0.5
print (delta[-1]/1000)





