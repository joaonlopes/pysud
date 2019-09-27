Acerca de
=========

pysud es una herramienta apuntada a ayudar en la creación de aventuras de texto
(al estilo de Collosal Cave por ejemplo) y librojuegos (como la serie de libros
de "Elige tu propia Aventura").

pysud es una librería orientada a objetos, que utiliza un bucle principal y un
mecanismo de eventos internos para distinguir cuando sucedió algo "interesante"
(ya sea el ingreso de un comando determinado, el uso de cierto objeto por parte
del jugador, etc.).

Por ahora provee clases para representar al juego, al jugador, a las
habitaciones que pudiera visitar y a los items que pudiera recoger. También
una jerarquía con eventos comunes (como agarrar un objeto, moverse de una habi-
tación a otra, etc.).

Componentes
===========

pysud.py        Módulo principal con clases como Game, Room, Item, etc
pysud_make.py   Módulo para generar datos de un nuevo juego. Los mismos se
                cargan desde dos ficheros xml: uno de configuración principal
                y otro que describe las habitaciones.
pysud_xml.py    Módulo utilizado por el make. Contiene los parseos xml.
gamemanager.py  Este módulo contiene una clase que mayormente lidia con la
                persistencia de objetos y "envuelve" a un objeto de clase Game.
events.py       Este módulo contiene la jerarquía de eventos que pueden suceder
                en un juego dado.

Licencia
========
pysud (todos los módulos que lo componen y las demos que los acompañan) se
lanzan bajo una licencia lgpl3. Vea los ficheros COPYING y COPYING.LESSER.

Para correr la demos
====================
Para correr demoscript_0 y demoscript_1 simplemente necesita ejecutar:

	~$ python3 demoscript_0.py
	~$ python3 demoscript_1.py

Para correr demoscript_2.py primero debe generar un fichero con los datos del
juego. Para eso se ejecuta pysud_make, asegurándose que las variables de
configuración global de este script (pysud_make.py) son:

	CONFIG_XML_PATH = 'config.xml'
	ROOMS_XML_PATH = 'rooms_demo2.xml'

Una vez verificado esto ejecute pysud_make:

	~$ python3 pysud_make.py

Esto debería haber generado un fichero game.dat en el mismo directorio donde
se encuentran los módulos de pysud y las demos.
Ahora puede ejecutar la demo con:

	~$ python3 demoscript_2.py

Contacto
========
francisco.pinchentti  (at)  gmail  (dot)  com
