import asyncio 
import time
from timeit import default_timer

li = [2,1,5,8558,9,8,36,1,859,98]
#li = [2,1]

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
        time.sleep(0.5)
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


def merge_sort2(valores):
    
    length = len(valores)
    
    if length == 0 or length == 1:
        time.sleep(0.5)
        return valores
    
    medio = int(length/2)
    #s1 = merge_sort(valores[0:medio])
    #s2 = merge_sort(valores[medio:length])
    
    s2 = merge_sort2(valores[medio:length])
    s1 = merge_sort2(valores[0:medio])
    
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

async def paralelo(lis):
    x = []
    loop = asyncio.get_running_loop()
    (resultados,_) = await asyncio.wait([loop.run_in_executor(None, merge_sort, i) for i in lis])

    for resultado in resultados:
        #print("El resultado es %s" % await resultado.result())
        x.append( resultado.result())
    return x

inicio =  default_timer()
merge_sort(li)
fin = default_timer()

inicio2 =  default_timer()
merge_sort2(li)
fin2 = default_timer()

print(merge_sort(li))

print("paralelo           " + str(fin - inicio))

print(merge_sort2(li))
print("normal             " + str(fin2 - inicio2))