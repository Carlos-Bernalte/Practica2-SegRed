# Practica 2


Se debe realizar un programa que averigüe la clave con la que se cifró el archivo dado. Este programa se puede realizar en cualquier lenguaje de programación. Se debe incluir en el entregable:

- Un README explicando cómo instalar y ejecutar el programa en un entorno GNU/Linux.
- El código fuente del programa.

Se valorará:

- La rapidez con la que se encuentra la clave: cuanto más rápido mejor.
- La limpieza del código y del contenido del proyecto.

# Diseño de la solución.
La primera idea fue cifrar un archivo gpg con una clave sencilla, y usar un script en python para comprobar que podíamos obtener la clave (cada clave se generaría al mismo tiempo de probar que sea la correcta) y a partir de ahí escalar el programa hasta poder usarlo con el archivo cifrado del campus.

Esta seria la función encargada de comprobar la clave en cuestion:
```python
def check_pass(password):
    try:
        subprocess.check_output(['gpg', '--batch', '--passphrase', password, '-d', 'archivo.gpg'], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return False
    except KeyboardInterrupt:
        sys.exit()
    else:
        return True

```

## Crear diccionarios
Una vez comprobado que el programa funciona, decidimos que, debido a que el tiempo de ejecución aumenta exponencialmente por cada carácter añadido a la clave, era necesario paralelizarlo mediante procesos/hilos. 

El problema de paralelizar el script, es que necesitamos asignarles un mismo espacio de claves a cada hilo para que la carga de trabajo sea equitativa. De esta manera decidimos separar el proceso de crear claves al margen de probarlas al instante.

Asi fue nuestra primera aproximación, el problema era asignarle al hilo algún 'argumento' para que generase el mismo número de claves distintas entre los demás hilos:
```python
def proceso(lenght):
    try:
        for password in itertools.product(CHARS, repeat=lenght):
            password = ''.join(password)
            if(check_pass(password)):
                print('La clave es: {}'.format(password))
                sys.exit()
    except KeyboardInterrupt:
        print('Saliendo...')
        sys.exit()

```

De esta manera, decidimos separar el programa tuviera dos funciones principales, la primera crearía n diccionarios con todas las combinaciones posibles repartidas equitativamente en ellos y la segunda parte se encargaría de leer los diccionarios y probar cada una de las claves.

A esta función se le pueden pasar por argumento el numero mínimo (por defecto si no se declara sera 1) y máximo de caracteres con los que deseamos trabajar. La idea es generar tantos diccionarios como cores tenga el ordenador en el que vayamos a ejecutar el programa en vez de generar solo uno, asi evitamos encontrarnos conn problemas de recursos compartidos entre hilos que puedan ralentizar o generar problemas en la ejecución. El proceso tendrá un poco mas de carga de trabajo pues en el caso en el que no sea exacta la división entre numero de combinaciones entre numero de procesos, se le asignara al últimos de estos el resto.
```python
def crear_dicc(n_processes, max_length, min_length=1):
    combinations=calc_combinations(max_length, min_length)//n_processes
    index=1
    x=1
    for i in range(min_length, max_length+1):
        for j in itertools.product(string.ascii_lowercase, repeat=i):
            
            password = ''.join(j)
            open('{}dicc_{}.txt'.format(DIR,index), 'a').write(password + '\n')
            if(x>=combinations and index<n_processes):
                index+=1
                x=1
            else:
                x+=1

```
Para calcular el número de claves por diccionario es necesario saber el número de posibles combinaciones según el mínimo y máximo introducidos para luego ser dividido entre el número de hilos que los leerán.
```python
def calc_combinations(max_length, min_length):
    combinations = 0
    for i in range(min_length, max_length+1):
        combinations += len(string.ascii_lowercase) ** i
    return combinations

```

## Averiguar la clave
El segundo script es el que intentara desencriptar el archivo con cada una de las claves generadas en los diccionarios, una vez más, lo mas eficiente es que tenga tantos hilos como cores tiene el ordenador a ejecutar.

Por ejemplo, generamos 16 diccionarios con las claves desde 1 a 4 caracteres. En total 475.254 claves, repartidas en 16 diccionarios habría unas 29.700 por diccionario, menos en el último, que habrá menos. Una vez generadas todas las claves, la segunda función asigna cada diccionario a un hilo diferente e intenta abrir el archivo con cada una de las claves del diccionario, hasta que lo consigue. 
```python
def pass_solver(i, file):
    try:
        start_time = time.time()
        with open('{}dicc_{}.txt'.format(DIR,i), 'r') as fichero:
            for password in fichero:
                if founded.value:
                    break
                password = password.rstrip('\n')
                if(check_pass(password, file)):
                    end_time = time.time()
                    print('[Proceso {}] Clave encontrada: {}'.format(i,password))
                    open('password.txt', 'a').write('clave: '+password +'\n'+'Tiempo de ejecución: '+calc_hora(end_time - start_time)+'\n')
                    sys.exit()
        end_time = time.time()
        print('[Proceso {}] No se encontró la clave. {}'.format(i, calc_hora(end_time - start_time)))
    except KeyboardInterrupt:
        print('[Proceso {}] Se ha interrumpido el proceso'.format(i))
        sys.exit()
```
Una vez un hilo consigue decodificar el archivo, todos los hilos paran, se imprime por pantalla la clave y se genera un archivo con la clave y el tiempo necesitado para obtenerla, ademas de que la variable compartida entre los hilos `founded.value` pasa a ser `True` con lo cual el resto de hilos pararan su ejecución.

# Resultados y conclusiones.
Una vez realizadas varias ejecuciones en ordenadores con distintas características hemos obtenido estos resultados.
| Número de procesos | Min longitud | Max longitud | Combinaciones posibles | Tiempo de ejecución |
|--------------------|--------------|--------------|------------------------|---------------------|
| 6                  | 1            | 1            | 26                     | 00:00:03            |
| 8                  | 1            | 2            | 702                    | 00:01:16            |
| 8                  | 1            | 5            | 12356630               | 4 días(aprox)       |
| 8                  | 4            | 4            | 456976                 | 5:58:40             |
| 16                 | 1            | 5            | 12356630               | 43h(aprox)          |
| 16                 | 4            | 4            | 456976                 | 1:45:58             |

Como podemos observar, en cuanto se tienen en cuenta claves de 5 cifras, el tiempo empleado en obtener la clave crece exponencialmente, por este motivo, estamos usando aproximaciones matemáticas en lugar de tiempos reales. 

Además, el tiempo de obtención de la clave varia en función de muchas variables, la mas importante son los hilos de ejecución, pero a veces también es cuestión de suerte encontrar la clave de una manera más rápida o no. Por ejemplo, la clave de la practica: `sgrd`, si generas 16 diccionarios de 4 caracteres máximo, la clave se encuentra aproximadamente en la mitad del diccionario, sin embargo, si generas 20, la clave se encuentra más al principio, por lo que el programa acabará antes. 

Una solución para esto sería coger claves aleatorias del diccionario y posteriormente eliminarlas, pero también aumentaría el tiempo de ejecución en cada intento. 

Otro problema del método utilizado es que si por ejemplo estamos buscando claves de 1 a 5 caracteres, pero la clave correcta tiene 4, todas las claves de 1, 2,3 y 4 caracteres estarían en el primer diccionario, mientras que las de 5 estarían en todos los demás. Si esto ocurre, realmente se esta perdiendo eficacia, ya que lo óptimo seria ir intentando las claves en orden ascendente de caracteres.
