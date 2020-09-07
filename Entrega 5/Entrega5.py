@author: joseberrios
"""
from leer_eof import leer_eof
from matplotlib.pylab import *
from satelite import satelite, satelite_J2, satelite_J2J3
from scipy.integrate import odeint
import datetime as dt
from eulerint import eulerint
from time import perf_counter
from sys import argv
from numpy import *

#nombre_eof = argv[1]
#t, x, y, z, vx, vy, vz =  leer_eof(nombre_eof)

t, x, y, z, vx, vy, vz =  leer_eof('S1B_OPER_AUX_POEORB_OPOD_20200826T111204_V20200805T225942_20200807T005942.EOF')




'''
------------------------------------------------------------------------------
            PREGUNTA 1
------------------------------------------------------------------------------
'''


figure(dpi=300)

# Grafico posicion realizado con funcion leer_eof, color azul

subplot(3,1,1)
title('Posición')
ylabel('$X$ (km)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
plot(t, x, c = 'blue', linewidth = 2)
tight_layout()

subplot(3,1,2)
ylabel('$Y$ (km)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
plot(t, y, c = 'blue', linewidth = 2)


subplot(3,1,3)
plot(t, z, c = 'blue', linewidth = 2)
ylabel('$Z$ (km)')
xlabel('Tiempo, t (horas)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))

# vector estado inicial

z0 = [x[0],y[0],z[0],vx[0],vy[0],vz[0]]

zf = [x[-1],y[-1],z[-1],vx[-1],vy[-1],vz[-1]]

t1 = perf_counter()

solucion = odeint(satelite, z0, t)

t2 = perf_counter()
# timepo que demora la funcion odeint
delta1 = t2 - t1

# Grafico posicion realizado con funcion odeint, color naranjo

subplot(3,1,1)
title('Posición')
ylabel('$X$ (km)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
plot(t, solucion[:,0], c = 'orange')
tight_layout()

subplot(3,1,2)
ylabel('$Y$ (km)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
plot(t, solucion[:,1], c = 'orange')

subplot(3,1,3)
plot(t, solucion[:,2], c = 'orange')
ylabel('$Z$ (km)')
xlabel('Tiempo, t (horas)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))

show()






'''
------------------------------------------------------------------------------
            PREGUNTA 2 y 3
------------------------------------------------------------------------------
'''


t3 = perf_counter()

solucion1 = eulerint(satelite, z0, t, Nsubdivisiones = 1)

t4 = perf_counter()
# tiempo que demora la funcion eulerint Nsubdivisiones = 1
delta2 = t4 - t3

t5 = perf_counter()

solucion2 = eulerint(satelite, z0, t, Nsubdivisiones = 250)

t6 = perf_counter()
# tiempo que demora la funcion eulerint Nsubdivisiones = 250
delta3 = t6 - t5



pos_odeint = solucion[:,0:3]
pos_eulerint = solucion1[:,0:3]
pos_eulerint1 = solucion2[:,0:3]

y_d = []
y_d1 = []


for i in range(len(pos_eulerint)):
    eul = ((pos_eulerint[i][0]**2 + pos_eulerint[i][1]**2 + pos_eulerint[i][2]**2)**0.5)
    ode = ((pos_odeint[i][0]**2 + pos_odeint[i][1]**2 + pos_odeint[i][2]**2)**0.5)
    eul1 = ((pos_eulerint1[i][0]**2 + pos_eulerint1[i][1]**2 + pos_eulerint1[i][2]**2)**0.5)
    y_d.append(eul-ode)
    y_d1.append(eul1-ode)
    
    
    
print (f'La deriva entre eulerint y odeint es de:','{0:.2f}'.format(y_d[-1]), 'm\n')
print (f'Tiempo demora función odeint: {delta1} s\n')
print (f'Tiempo demora función eulerint (Nsubidvisiones = 1): {delta2} s\n')
print (f'Tiempo demora función eulerint (Nsubidvisiones = 250): {delta3} s')
    
figure(dpi=300)

# Grafico deriva entre funcion eulerint y odeint

plot(t, y_d)
title(f'Distancia entre posición odeint y eulerint (Ns=1), $\\delta_{{max}}$'+' {0:.2f}'.format(y_d[-1]/1000)+' (km)')
ylabel('Deriva, $δ$ (km)')
xlabel('Tiempo, t (horas)')
yticks((0,1e6,2e6,3e6,4e6,5e6,6e6,7e6),('0','1000','2000','3000','4000','5000','6000','7000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
tight_layout()
show()

figure(dpi=300)

# Grafico deriva entre funcion eulerint (Nsubdivisiones = 250) y odeint

plot(t, y_d1)
title(f'Distancia entre posición odeint y eulerint (Ns=250), $\\delta_{{max}}$'+' {0:.2f}'.format(y_d1[-1]/1000)+' (km)')
ylabel('Deriva, $δ$ (km)')
xlabel('Tiempo, t (horas)')
yticks((0,1e4,2e4,3e4,4e4,5e4,6e4),('0','10','20','30','40','50','60'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
tight_layout()
show()








'''
------------------------------------------------------------------------------
            PREGUNTA 4
------------------------------------------------------------------------------
'''

T = perf_counter()

solucion3 = odeint(satelite_J2,z0,t)
solucion4 = odeint(satelite_J2J3,z0,t)

pos_odeint2 = solucion3[:,0:3]
pos_odeint3 = solucion4[:,0:3]

figure(dpi=300)

subplot(3,1,1)
ylabel('$X$ (km)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
plot(t, x, c = 'blue')
tight_layout()

subplot(3,1,2)
ylabel('$Y$ (km)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
plot(t, y, c = 'blue')


subplot(3,1,3)
plot(t, z, c = 'blue')
ylabel('$Z$ (km)')
xlabel('Tiempo, t (horas)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))

subplot(3,1,1)
title('Posición con J2')
ylabel('$X$ (km)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
plot(t, solucion3[:,0], c = 'orange')
tight_layout()

subplot(3,1,2)
ylabel('$Y$ (km)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
plot(t, solucion3[:,1], c = 'orange')

subplot(3,1,3)
plot(t, solucion3[:,2], c = 'orange')
ylabel('$Z$ (km)')
xlabel('Tiempo, t (horas)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))

show()

figure(dpi=300)

subplot(3,1,1)
ylabel('$X$ (km)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
plot(t, x, c = 'blue')
tight_layout()

subplot(3,1,2)
ylabel('$Y$ (km)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
plot(t, y, c = 'blue')


subplot(3,1,3)
plot(t, z, c = 'blue')
ylabel('$Z$ (km)')
xlabel('Tiempo, t (horas)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))

subplot(3,1,1)
title('Posición con J2J3')
ylabel('$X$ (km)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
plot(t, solucion4[:,0], c = 'orange')
tight_layout()

subplot(3,1,2)
ylabel('$Y$ (km)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
plot(t, solucion4[:,1], c = 'orange')

subplot(3,1,3)
plot(t, solucion4[:,2], c = 'orange')
ylabel('$Z$ (km)')
xlabel('Tiempo, t (horas)')
yticks((-5000000, 0, 5000000),('-5000', '0', '5000'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))

show()






pos = [x,y,z]
pos_ode = solucion
pos_J2 = pos_odeint2
pos_J2J3 = pos_odeint3

y_deriva = []
y_deriva1 = []
y_deriva2 = []


    
for i in range(len(pos_eulerint)):
    po_ode1 = ((pos[0][i]-pos_ode[i][0])**2 + (pos[1][i]-pos_ode[i][1])**2 + (pos[2][i]-pos_ode[i][2])**2)**0.5
    po = ((pos[0][i]**2 + pos[1][i]**2 +pos[2][i]**2)**0.5)
    po_ode = ((pos_ode[i][0])**2 + (pos_ode[i][1])**2 + (pos_ode[i][2])**2)**0.5
    po_J2 = ((pos_J2[i][0])**2 + (pos_J2[i][1])**2 + (pos_J2[i][2])**2)**0.5
    po_J2J3 = ((pos_J2J3[i][0])**2 + (pos_J2J3[i][1])**2 + (pos_J2J3[i][2])**2)**0.5
    y_deriva.append(abs(po_ode1))
    y_deriva1.append(abs(po-po_J2))
    y_deriva2.append(abs(po-po_J2J3)) 
    
    
    
    
    
figure(dpi=300)

plot(t, y_deriva)
title(f'Distancia entre posición real y predicha, $\\delta_{{max}}$'+' {0:.2f}'.format(y_deriva[-1]/1000)+' (km)')
ylabel('Deriva, $δ$ (km)')
xlabel('Tiempo, t (horas)')
yticks((0,1e5,2e5,3e5,4e5),('0','100','200','300'))
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
tight_layout()
show()

figure(dpi=300)

plot(t, y_deriva1)
title(f'Distancia entre posición real y predicha J2, $\\delta_{{max}}$'+' {0:.2f}'.format(y_deriva1[-1]/1000)+' (km)')
ylabel('Deriva, $δ$ (km)')
xlabel('Tiempo, t (horas)')
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
tight_layout()
show()

plot(t, y_deriva2)
title(f'Distancia entre posición real y predicha J2J3, $\\delta_{{max}}$'+' {0:.2f}'.format(y_deriva2[-1]/1000)+' (km)')
ylabel('Deriva, $δ$ (km)')
xlabel('Tiempo, t (horas)')
xticks((0,18000,36000,54000,72000,90000),('0','5','10','15','20','25'))
tight_layout()
show()

T2 = perf_counter()


print(f'Tiempo total utilizado en ejecutar la pregunta 4: {T2-T} s')
