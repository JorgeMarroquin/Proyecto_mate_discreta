from tkinter import *
from tkinter import filedialog
import asyncio
import time
import os
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
    listas = []
    for x in lineas:
        y = list(x[0])
        listas.append([int(z) for z in y])

    async def aux(iz, der):
        loop = asyncio.get_running_loop()
        t1 = loop.run_in_executor(None, merge_sort, iz)
        t2 = loop.run_in_executor(None, merge_sort, der)
        res1 = await t1
        res2 = await t2
        return [res1, res2]

    def merge_sort(valores):
        
        length = len(valores)
        
        if length == 0 or length == 1:
            return valores
        
        medio = int(length/2)
        temp = asyncio.run(aux(valores[medio:length], valores[0:medio]))
        
        s2 = temp [0]
        s1 = temp [1]
        
        i = 0
        j = 0
        resultado = []
        
        while(i < len(s1) or j < len(s2)):
            
            if i >= len(s1):
                resultado.append(s2[j])
                j = j + 1
            elif j >= len(s2) or s1[i] <= s2[j]:
                resultado.append(s1[i])
                i = i + 1
            else:
                resultado.append(s2[j])
                j = j + 1
        return resultado

    async def inicio():

        filename = filedialog.asksaveasfilename(defaultextension=".txt", title= 'Selecciona el lugar para guardar las listas ordenadas.', filetypes = [('Arcivo de texto', '.txt')])
        if filename == '':
            return 0
        filer = open(filename,"w")
        loop = asyncio.get_running_loop()
        (resultados,_) = await asyncio.wait([loop.run_in_executor(None, merge_sort, i) for i in listas])

        for resultado in resultados:
            y = "".join([str(_) for _ in resultado.result()])
            filer.write(y + "\n")

        print("Listas guardadas y ordenadas exitosamente en:")
        print(filename)
        print("\n")


    if __name__ == '__main__':
        asyncio.run(inicio())

    

main_program()

print("Gabriel Chavarria 20181386")
print("jorge Marroquín   20181358")
print("Juan Cáceres      20181049")
print(" ")
input('Presiona enter para ternimar')
