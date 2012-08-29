Taller-de-sorting
=================


Bueno, te cuento. La idea es asi. Hay parte del codigo que te voy a mandar, que le vas a dar a los alumnos , otra parte es para recibir submits de ellos y otra es para hacer las animaciones de sorting.

1) Instalacion
       - sudo apt-get install  python-setuptools
       - despues anda al taller de sorting, busca el archivo setup.py y hace
          sudo python setup.py install 

2) Codigo de los alumnos
Como queremos que los alumnos hagan un algoritmo n^2 y otro n log n, y esten parejos, hice un script que genera el codigo que se tiene que bajar cada grupo para que quede mas o menos balanceado (igual no te va a quedar, porque algunos algoritmos son mas dificiles je)
Ese script se llama build_alumni_distr.py.
           python build_alumni_distr.py 20 -> te mete 20 archivos en la carpeta alumni_distrs
Esa carpeta tenes que compartirla. En lo que te mando ya hay 20 archivos, asi que no creo que tengas que correrlo de nuevo

1.bis) Los alumnos pueden probar el codigo, para eso hice un script que esta en lo que les mandas por mail. Ese script te prueba el codigo con arreglos chiquitos y con arreglos grandes. Ademas podes pedirle que te estime la constante de tu algoritmo (a ojo de buen cubero =p) pero es ludico.

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

por ejemplo python test.py quicksort -l

3) Submit de codigo
   a) Setup: para submitear los alumnos te van a mandar mail a mdsafe+taller@gmail.com. Eso te va a llegar a tu direccion de correo, pero podes poner un filtro de mensajes para que te los mande a una carpeta llamada "taller sorting". Es importante que le pongas exactamente ese nombre sin cambiar mayusculas ni nada.
   b) Submit: Los alumnos te tienen que mandar un mail a mdsafe+taller@gmail.com con el archivo algorithms.py como attach. Solo ese archivo.
   b) Downloads: Cuando los alumnos te manden soluciones, hace python download_submits.py mdsafe@gmail.com. Eso te va a pedir tu password, y te juro por que me caiga un rayo que no te lo voy a robar, solo se usa para bajar los mails del taller =p

4) Interfaz web
     a) Setup: Para mostrar las animaciones, lo hice con una interfaz web, porque es lo que se hacer (no se hacer otras interfaces =p). Lo que tenes que hacer es python webi/controllers.py
     b) Uso: Despues que la levantaste entra en localhost:8080 y vas a ver una hermosa pagina web (?). Ahi tenes una lista desplegable con todos los algoritmos. Si elegis un algoritmo te pone todas las implementaciones que tiene de ese algoritmo. Tambien podes poner "Custom" para elegir una combinacion que se te antoje. Trata de usarlo desde Chrome porque anda mas rapido. 
Ademas tenes dos sliders, uno para el tamaño del arreglo y otro para la velocidad de sorting. 


Te recomiendo que pruebes todo un par de dias antes por si las dudas. Por probar todo me refiero tambien a poner la regla de mensajes y mandarte a vos mismo mails, bajarlos y usarlos. O sea, todo el ciclo.

Por ultimo te estoy mandando dos apuntes, uno con invariantes y otro con sintaxis de python. 
Es importante que los alumnos en los algoritmos no construyan nuevas listas, porque la forma que tengo para contar operaciones es armandome yo una lista. Mira el archivo list.py


Bueno, cualquier cosa avisame. Estoy pensando en armar un pdf con toda esta explicacion =p

