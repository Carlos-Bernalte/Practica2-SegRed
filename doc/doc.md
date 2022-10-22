# Seguridad en redes

	Práctica 2: Obtener la contraseña de un archivo cifrado con gpg mediante fuerza bruta.
	


# Diseño de la solución.
La primera idea es cifrar un archivo gpg con una clave sencilla, y usar un programa python para comprobar que podemos obtener la clave y a partir de ahí escalar el programa hasta poder usarlo con el archivo cifrado del campus.

Una vez comprobado que el programa funciona, decidimos que, debido a que el tiempo de ejecución aumenta exponencialmente por cada carácter añadido a la contraseña, es necesario paralelizarlo mediante hilos. 

Una vez tenemos paralelizado mediante hilos el programa, comprobamos que necesitamos manejar el espacio de claves de una manera más eficiente, por lo que decidimos crear diccionarios de claves.

De esta manera, el programa tiene dos funciones principales: crea n diccionarios con todas las combinaciones posibles repartidas equitativamente en ellos. A esta función se le pueden pasar por argumento el numero mínimo y máximo de caracteres con los que deseamos trabajar. La idea es generar tantos diccionarios como cores tenga el ordenador en el que vayamos a ejecutar el programa. 

La segunda función es la que intentara desencriptar el archivo con cada una de las claves generadas en los diccionarios, una vez más, lo mas eficiente es que tenga tantos hilos como cores tiene el ordenador a ejecutar.

Por ejemplo, generamos 16 diccionarios con las claves desde 1 a 4 caracteres. En total 475.254 claves, repartidas en 16 diccionarios habría unas 29.700 por diccionario, menos en el último, que habrá menos. Una vez generadas todas las claves, la segunda función asigna cada diccionario a un hilo diferente e intenta abrir el archivo con cada una de las claves del diccionario, hasta que lo consigue. Una vez un hilo consigue decodificar el archivo, todos los hilos paran, se imprime por pantalla la contraseña y se genera un archivo con la contraseña y el tiempo necesitado para obtenerla.

# Resultados y conclusiones.
Una vez realizadas varias ejecuciones en ordenadores con distintas carácteristicas hemos obtenido estos resultados.
| Número de procesos | Min longitud | Max longitud | Combinaciones posibles | Tiempo de ejecución |
|--------------------|--------------|--------------|------------------------|---------------------|
| 8                  | 1            | 5            | 12356630               |     4 dias (aprox)                |
| 8                  | 4            | 4            | 456976                 | 5:58:40             |
| 16                 | 1            | 5            | 12356630               |    43h(aprox)         |
| 16                 | 4            | 4            | 456976                 | 1:45:58             |

Como podemos observar, en cuanto se tienen en cuenta claves de 5 cifras, el tiempo empleado en obtener la clave crece rápidamente, por este motivo, estamos usando aproximaciones matemáticas en lugar de tiempos reales. 

Además, el tiempo de obtención de la clave varia en función de muchas variables, la mas importante son los hilos de ejecución, pero a veces también es cuestión de suerte encontrar la clave de una manera más rápida o no. Por ejemplo, la clave de la practica: sgrd, si generas 16 diccionarios de 4 caracteres máximo, la clave se encuentra aproximadamente en la mitad del diccionario, sin embargo, si generas 20, la clave se encuentra más al principio, por lo que el programa acabará antes. 

Una solución para esto sería coger claves aleatorias del diccionario y posteriormente eliminarlas, pero también aumentaría el tiempo de ejecución en cada intento. 

Otro problema del método utilizado es que si por ejemplo estamos buscando claves de 1 a 5 caracteres, pero la clave correcta tiene 4, todas las claves de 1, 2,3 y 4 caracteres estarían en el primer diccionario, mientras que las de 5 estarían en todos los demás. Si esto ocurre, realmente se esta perdiendo eficacia, ya que lo óptimo seria ir intentando las claves en orden ascendente de carácteres.


