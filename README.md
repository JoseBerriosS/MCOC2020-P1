# MCOC2020-P1
# Balística
Gráfico en el cual se trazan 3 trayectorias de un mismo proyectil, pero con diferentes vientos.

![Balistica](https://user-images.githubusercontent.com/69157278/91086860-7fc0c000-e61d-11ea-9b90-033362e050ff.png)

# Satélite
A continuación se presenta la historia de tiempo para x(t), y(t) y z(t). Se puede observar que el problema se abordo como un problema en 2D, es por eso que z(t) permanece en 0.
![Historia_tiempo](https://user-images.githubusercontent.com/69157278/91518830-11029180-e8bf-11ea-8556-b8ca3742194b.png)


Si bien son más de dos órbitas, la linea verde demarca la superficie terrestre, la velocidad ajustada del satelite estuvo cerca de los 666 m/s.

![distancia](https://user-images.githubusercontent.com/69157278/91518835-1364eb80-e8bf-11ea-807c-32058eacb589.png)


En este grafico se logra apreciar la trayectoria del satelite alrededor de la superficie de la tierra.
![trayectoria](https://user-images.githubusercontent.com/69157278/91518838-14961880-e8bf-11ea-8b54-147fa8428848.png)


# integracion edm avanzada

![Posicion](https://user-images.githubusercontent.com/69157278/92385528-70934500-f0e8-11ea-880d-1d1b2afda91a.png)

Se ve como los resultados predichos con odeint de la orbita calzan con los resultados exactso del archivo EOF


![Deriva_eulerint_odeint](https://user-images.githubusercontent.com/69157278/92385537-74bf6280-f0e8-11ea-881d-8a030aed0045.png)

Se ve que ambos algoritmos distan mucho entre si, aqui claramente el problema es que las subdivisiones de eulerint deben ser mucho mayores. Aqui la funcion eulerint se demoró : 0.8234631490049651 s (Ns = 1)


![Deriva_eulerint_odeint_ns3000](https://user-images.githubusercontent.com/69157278/92386075-7178a680-f0e9-11ea-9f16-5af9dbabf37d.png)

La cosa cambia aquí (Ns = 3000), ya que ahora baja considerablemente la distancia entre ambos algoritmos, pero se sacrifica el tiempo, ya que tardó: 1288.657286132002 s

![Deriva_real_predicha](https://user-images.githubusercontent.com/69157278/92385545-77ba5300-f0e8-11ea-8942-4681cd75306d.png)

La deriva de la funcion odeint sin mejorar ya es bastante buena.


![PosicionJ2](https://user-images.githubusercontent.com/69157278/92385553-7a1cad00-f0e8-11ea-95be-20d5b44f3d06.png)
![PosicionJ2J3](https://user-images.githubusercontent.com/69157278/92385547-7852e980-f0e8-11ea-98e6-da11061eb956.png)

Con los terminos J2 y J3 no cambia mucho, ya que la diferencia se encuntra si acercamos mas la grafica.

![Deriva_real_predichaJ2](https://user-images.githubusercontent.com/69157278/92385544-7721bc80-f0e8-11ea-9870-8a34a68cf16e.png)

La deriva utilizando J2
  
  
![Deriva_real_predichaJ2J3](https://user-images.githubusercontent.com/69157278/92385539-75f08f80-f0e8-11ea-87fe-f2a253cdaa7b.png)

La deriva utilizando los terminos J2 y J3. El tiempo que tarda en ejecutar el código para este problema (Odeint sin mejorar y mejorado) es: 1.8222070049960166 s


# Entrega Final Satélite 

Al agregar el termino J4 y J5, no hya una mejora sustancial. Al momento de probar el código, arrojo 2,11 km para el archivo dado. Luego al probarlo con el "3.EOF" que subió el profesor, llego a 8 km aprox. ¿Con más términos pudo haber mejorado? Probablemente, pero requiere más tiempo.


