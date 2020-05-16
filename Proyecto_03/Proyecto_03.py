import networkx as nx

import matplotlib.pyplot as plt

option = {'with_labels': True}

from tkinter import *
from tkinter import filedialog
import asyncio
import time
import os
import copy
from timeit import default_timer

#escoger el archivo
file = filedialog.askopenfile(title= 'Selecciona el archivo con las listas a ordenar')
if file:
    print(file.name)
    nombre = file.name



def main_program():

    with open(nombre,'r') as f:
            lista_todos_elementos = f.readlines()

    #para quitar los espacios entre los numeros
    lineas = []
    for x in lista_todos_elementos:
        listas_elementos_separados = x.split()
        lineas.append(listas_elementos_separados)

    #ocnvierte las líneas en listas de números
    G=nx.Graph()
    listas = []
    for x in lineas:
        listas.append(str(x[0]))
    
    listas.sort()
    nod = []
    for x in listas:
        if x[0] == '+':
            G.add_node(x[1:])
            nod.append(x[1:])
        elif x[0] == '-' and x[1:] in listas:
            G.remove_node(x[1:])

    def binario(lista, respuesta = []):            #la función crea una lista con el punto medio total, conectado con el punto pedio de dos listas las cuales están del lado
        if len(lista) == 1:                         #derecho del centro y de lado izquirdo al centro y se hace recursión
            return []
        elif len(lista) == 2:
            return [(lista[0],lista[1])]
        else:
            medio = int(len(lista)/2)
            s2 = lista[medio+1:len(lista)]
            s1 = lista[:medio]
            medio2 = int(len(s1)/2)
            medio3 = int(len(s2)/2) + medio +1
            respuesta.append((lista[medio], lista[medio2]))
            respuesta.append((lista[medio], lista[medio3]))
            iz = binario(s1,[])
            der = binario(s2,[])
            respuesta = respuesta + iz + der
            return respuesta
    edg = binario(nod)
    for x in edg:
        G.add_edge(*x)
    
    nx.draw(G, **option)

#Se muestra en pantalla

    plt.show()

    

main_program()

print("Gabriel Chavarria 20181386")
print("jorge Marroquín   20181358")
print("Juan Cáceres      20181049")
print(" ")
input('Presiona enter para ternimar')


