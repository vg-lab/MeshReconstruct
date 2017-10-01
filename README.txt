
- autor: Juan Morales del Olmo
- proyecto: Cajal Blue Brain <http://cajalbbp.cesvima.upm.es/>


MESH REPAIR
===========

Este repositorio contiene varios programas

1.- compute_areas.py es el script que calcula las áreas de los objetos que encuentre en los VRML de entreada
2.- gui.py es una interfaz gráfica para compute_areas.py
3.- repair_mesh.py es un script que antes de calcular las áreas hace un close para unir los diferentes parches de los objetos en el VRML


Experimento Original
====================

El fichero if6 2 0-2 enero VOLS.vrml es un VRML de las mallas que sacaban con el método tradicional. 

Tienen el problema de que hay espinas que están divididas en diferentes superficies porque aplicaron varios thresholds.

Lo que quieren calcular es la superficie de las espinas... no hace falta que sea individualmente. El valor acumulado valdría.




