import re
from tkinter import *
from tkinter import filedialog


#escoger el archivo
file = filedialog.askopenfile(title= 'Selecciona un mapa')
if file:
    print(file.name)
    nombre = file.name

def main_program():
    #abre el mapa
    with open('mapa.txt','r') as f:
            lista_todos_elementos = f.readlines()

    #para quitar los espacios entre los numeros
    lista = []
    for x in lista_todos_elementos:
        listas_elementos_separados = x.split()
        lista.append(listas_elementos_separados)
        
    #Probabilidad de las 2 primeras líneas
    def copiar(lista):
        res = re.match("(^(?P<uno>[0-9]{2})\s(?P<dos>[0-9]{2})\s(?P<tres>[0-9]{2})\s(?P<cua>[0-9]{2}))", lista)
        
        return (float(res.group('uno'))/100, float(res.group('dos'))/100, float(res.group('tres'))/100, float(res.group('cua'))/100)
        
    line1 = " ".join(lista[0])
    (A_SB, B_SB, P_SB, O_SB) = copiar(line1)

    line2 = " ".join(lista[1])
    (A_SP, B_SP, P_SP, O_SP) = copiar(line2)

    #tamaño del mapa
    for horizontal in lista[2]:
        tamaño_horizontal = int(horizontal)

    for vertical in lista[3]:
        tamaño_vertical = int(vertical)

    #Para el conteo de los pisos del mapa
    total_pisos = tamaño_vertical * tamaño_horizontal

    lista_mapa = []
    lista_mapa = lista_todos_elementos[4:4+tamaño_vertical]

    #conteo de pisos
    def conteo_piso_especifico(caracter):
        flag = True
        conteo = 0
        conteo_total = 0
        while flag:
            contar_p = lista_mapa[conteo].count(caracter)
            conteo_total += contar_p
            conteo += 1
            if conteo > len(lista_mapa) -1:
                flag = False
        return conteo_total

    #probailiad de pisos
    P_A = float(conteo_piso_especifico('A')/(tamaño_horizontal*tamaño_vertical))
    P_B = float(conteo_piso_especifico('B')/(tamaño_horizontal*tamaño_vertical))
    P_P = float(conteo_piso_especifico('P')/(tamaño_horizontal*tamaño_vertical))
    P_O = float(conteo_piso_especifico('O')/(tamaño_horizontal*tamaño_vertical))

    #para las peticiones
    lista_peticiones = lista[4+tamaño_vertical:]

    #peticiones simples
    def peticiones_simples(caracter):
            if len(caracter) == 1 :
                probabilidad_simple = conteo_piso_especifico(caracter)/total_pisos
                return probabilidad_simple

    def unir(letra):
        if letra == 'A':
            return([P_A, A_SB, A_SP])
        if letra == 'B':
            return([P_B, B_SB, B_SP])
        if letra == 'P':
            return([P_P, P_SB, P_SP])
        if letra == 'O':
            return([P_O, O_SB, O_SP])
            
    def total(letra):
        if letra == 'SP':
            return(P_A*A_SP + P_B*B_SP + P_P*P_SP + P_O*O_SP)
        if letra == 'SB':
            return(P_A*A_SB + P_B*B_SB + P_P*P_SB + P_O*O_SB)
        if letra == '!SP':
            return(P_A*complemento(A_SP) + P_B*complemento(B_SP) + P_P*complemento(P_SP) + P_O*complemento(O_SP))
        if letra == '!SB':
            return(P_A*complemento(A_SB) + P_B*complemento(B_SB) + P_P*complemento(P_SB) + P_O*complemento(O_SB))

    #OPERADORES
    def complemento(num):
        return 1 - num

    def analizar(pregunta):
        if pregunta[0] == '!' and pregunta[1] != 'S':
            return (complemento(peticiones_simples(pregunta[1])))
        if pregunta[0] == '!' and pregunta[1] == 'S':
            x = unir(pregunta[len(pregunta) - 1])
            if pregunta[1:3] == 'SB':
                return (complemento(x[1])) 
            elif pregunta[1:3] == 'SP':
                return (complemento(x[2]))
        if pregunta[0] != '!' and pregunta[0] == 'S':
            x = unir(pregunta[len(pregunta) - 1])
            if pregunta[0:2] == 'SB':
                return x[1] 
            elif pregunta[0:2] == 'SP':
                return x[2]
                
    def andor(piso, condicion):
        p = unir(piso)
        if ',' in condicion:
            x = condicion.index(',')
            e1 = str(condicion[0:x])
            e2 = str(condicion[x+1:])
            y = float(analizar(str(e1) + str(piso)) or 0) * float(analizar(str(e2) + str(piso)) or 0)
            z = total(e1) * total(e2)
            return [float(y), float(z)]
        elif ';' in condicion:
            x = condicion.index(';')
            e1 = str(condicion[0:x])
            e2 = str(condicion[x+1:])
            y = float(analizar(str(e1) + str(piso)) or 0) + float(analizar(str(e2) + str(piso)) or 0)
            z = total(e1) + total(e2) - (total(e1) * total(e2))
            return [float(y), float(z)]
    #=============================================================================================
    def bayes(probab):
        i = probab[0]
        d = probab[2:]
        x = unir(i)
        y = total(d)
        if d == 'SB':
            PBA = x[0]*x[1]
            return(PBA/y)
        if d == '!SB':
            PBA = x[0]* complemento(x[1])
            return(PBA/y)
        if d == 'SP':
            PBA = x[0]*x[2]
            return(PBA/y)
        if d == '!SP':
            PBA = x[0]* complemento(x[2])
            z = total(d)
            return(PBA/y)
        if len(d) > 3:
            extra = andor(i, d)
            return((x[0]*extra[0])/extra[1])
        else: return None

    def pruebas(pru):
        if bayes(pru) != None:
            return bayes(pru)
        elif peticiones_simples(pru) != None:
            return peticiones_simples(pru)
        elif analizar(pru) != None:
            return analizar(pru)

    for z in lista_peticiones:
        inp = "".join(z[0])
        probabilidad = float(pruebas(inp) or 0)
        print("La probabilidad de " + inp + " es " + str(probabilidad))
main_program()
print("Gabriel Chavarria 20181386")
print("jorge Marroquín   20181358")
print("Juan Cáceres      20181049")
print(" ")
input('Presiona enter para ternimar')