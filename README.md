Taller de sorting
=================


Instalación
-----------
 * sudo apt-get install  python-setuptools
 * sudo python setup.py install. Si se utiliza [virtualenv](http://pypi.python.org/pypi/virtualenv) se puede evitar ser sudo
 * Una vez instalado el paquete, se dispondrán de un set de comandos system wide. Ejecutar `taller-sorting-config`


Explicación del código
----------------------

El código se divide en 3 partes:
 * La que se le entrega a los alumnos para que trabajen
 * Para recibir los submits de los alumnos
 * Para visualizar los algoritmos
 
### Código de los alumnos
Dado que queremos que los alumnos hagan un algoritmo n^2 y otro n log n, y esten parejos, se cuenta con un script que genera el código que se tiene que bajar cada grupo de forma tal que queden razonablemente balanceados entre los grupos. 
Para ejecutarlo correr `taller-sorting-build-alumni-distr N`, donde N es la cantidad de grupos. Creará la carpeta `alumni_distrs` con una
carpeta por grupo.

Para que los alumnos prueben el código, se cuenta con un script que dentro de lo que cada alumno descarga. Ese script prueba el código con arreglos pequeños y con medianos. Además cuenta con una opción para estime la constante de tu algoritmo. Si bien la estimación es rudimentaria, también es lúdica.

<pre>
grupo_1: python test.py --help
Usage: test.py algoritmo [options]

Options:
  -h, --help            show this help message and exit
  -l, --listita         ejecuta tu algoritmo con una lista chiquita
  -L, --listota         ejecuta tu algoritmo con una lista grandota
  -g GROUP_NAME, --grupo=GROUP_NAME
                        En caso de ambiguedad, el nombre del grupo
  -e, --estimar-constantes
                        Si tu algoritmo es n*log(n) o n^2, trata de estimar la
                        constante

</pre>

Ejemplo: `python test.py quicksort -l`

Para que esto ande, es *importante* que los alumnos utilicen la implementación dada de la clase lista (archivo lista.py), puesto 
que hace un conteo de accesos y escrituras. Esto se utiliza tanto para estimar la constante como para visualizar desde la interfaz 
gráfica. De modo que si los alumnos crean listas nuevas el conteo se verá perdido.

En el caso de necesitar un arreglo temporal, la lista cuenta con un método `crear_temporal` que crea una lista del mismo tamaño que 
la lista a la que se llama el método. Este método está pensado para el paso de merge del merge sort. 

### Submit de soluciones
 * **Setup**: para submitear los alumnos deberán mandar por mail su solución. Por ejemplo a anonimo+taller@gmail.com. Los mails escritos a esa dirección, llegarán a anonimo@gmail.com, por lo que los puede filtrar facilmente. 
    Es necesario filtrar esos mails y asignarles una etiqueta con el exactamente el nombre "taller sorting". Dado que los filtros son
    case sensitive, es importante que se llame exactamente asi.
 * **Submit**: Los alumnos deben enviar un mail a anonimo+taller@gmail.com con el archivo algorithms.py como attach. Solo ese archivo.
 * **Downloads**: Cuando los alumnos envien sus soluciones, ejecutar taller-sorting-download-submits.py anonimo@gmail.com. El programa luego pide el password para acceder a esa cuenta de mail. Sólo se utiliza el password para ese fin. En caso de desconfiar se invita a utilizar otra cuenta de mails o revisar el codigo.
 * **Recover**: en caso de necesitar las soluciones, el comando taller-sorting-algorithms especificará en que directorio se guardaron

### Interfaz web
 * **Setup**: Para mostrar las animaciones es necesario levantar el servidor web. Para eso se debe ejecutar `taller-sorting-webi`.
 * **Uso**: Una vez levantada la aplicación, abrir en un navegador la dirección `localhost:8080`. En ella se encuentra una lista desplegable con todos los algoritmos. Si se elige un algoritmo, se cargan te todas las implementaciones que los alumnos enviaron de ese algoritmo. También da una opción de elegir "Custom" para visualizar una combinación arbitraria. Se recomienda el uso de Chrome dado que la animación hace un uso intensivo de javascript.



