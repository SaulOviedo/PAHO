#
# Este es el Algoritmo mucho mas eficiente Realizado
# Partiendo Del intento Pasado
# funciona unas 100 veces mas rapido
#


import Iniciador
import numpy as np
from itertools import combinations
from random import sample
##Materias de prueba

'''
MATERIAS= {
"DHP":{1:[(1,7),(1,8)],2:[(1,9),(1,10)],3:[(1,11),(1,12)],4:[(1,14),(1,15)]},
"LAB":{1:[(1,7),(1,8)],2:[(1,9),(1,10)],3:[(1,11),(1,12)],4:[(1,14),(1,15)]},
"CALCULO":{1:[(1,7),(1,8)],2:[(1,9),(1,10)],3:[(1,11),(1,12)],4:[(1,14),(1,15)]},
"CIRCUITOS":{1:[(1,7),(1,8)],2:[(1,9),(1,10)],3:[(1,11),(1,12)],4:[(1,14),(1,15)]}
}
'''

MATERIAS= Iniciador.MATERIAS
PROFESORES= Iniciador.PROFESORES
CAREERS= Iniciador.CAREERS

Secciones= []
for code in MATERIAS:
    Secciones.append([MATERIAS[code]['name'],len(MATERIAS[code]['secciones']), CAREERS[code], code])
Secciones.sort()

## metodos para buscar horarios
## retorna Nombre, secciones, formatos, posibilidades

def posibleHorario(materiasCode,SeccOblig=[]):
    materias = []
    materiasName = [MATERIAS[code[0]]['name'] for code in SeccOblig] + [MATERIAS[code]['name'] for code in materiasCode]
    oblig=[]
    numSecc=[]
    iniciaArray=[]
    horario=[]
    maxCantidad=10
    seccionesFinal=[]
    ## iniciando variables
    for code in materiasCode:
        materias.append(MATERIAS[code]['secciones'])

    for course in SeccOblig:
        oblig+=MATERIAS[course[0]]['secciones'][course[1]]
        #materiasObl.append(course[0])
        numSecc.append(course[1])

    for i in range(len(materias)):
        iniciaArray.append(len(materias[i]))


    ### Aquii hacemos las combinaciones
    if not check(oblig):
        return []
    muestra=[]
    if len(materiasCode)==1:
        for a in MATERIAS[materiasCode[0]]['secciones']:
             if check(oblig[:]+MATERIAS[materiasCode[0]]['secciones'][a]):
                seccionesFinal.append(numSecc+[a])
        cantidad = len(seccionesFinal)
        if cantidad == 0:
            return []
        if cantidad >= maxCantidad:
            cantidad=maxCantidad
            muestra= sample(range(cantidad),maxCantidad)
        else:
            muestra=range(cantidad)
    else:
        posible= np.full(iniciaArray,True,dtype=bool)
        combi= list(combinations(range(len(materias)),2))
        nulo=slice(None)
        for c in combi:
            for a in MATERIAS[materiasCode[c[0]]]['secciones']:
                for b in MATERIAS[materiasCode[c[1]]]['secciones']:
                    if not check(oblig[:] + MATERIAS[materiasCode[c[0]]]['secciones'][a]+MATERIAS[materiasCode[c[1]]]['secciones'][b]):
                        temp=[]
                        for i in range(len(iniciaArray)):
                            if i==c[0]:
                                temp.append(a-1)
                            elif i == c[1]:
                                temp.append(b-1)
                            else:
                                temp.append(nulo)
                        if len(iniciaArray) == 2:
                            posible[tuple(temp)]=False
                        else:
                            posible[tuple(temp)].fill(False)
        resultado = np.array(np.where(posible))+1
        cantidad= resultado.shape[1]
        if cantidad == 0:
            return []
        parteOblig= np.repeat(numSecc,cantidad).reshape(len(numSecc),cantidad)
        seccionesFinal = np.vstack((parteOblig,resultado)).T.astype(int)
        if cantidad > maxCantidad:
            cantidad=maxCantidad
            muestra= sample(range(cantidad),maxCantidad)
        else:
            muestra=range(cantidad)

    materiasCode = [code[0] for code in SeccOblig] + materiasCode
    horas=['7:05 a 7:55','8:00 a 8:50','8:55 a 9:45','9:50 a 10:40','10:45 a 11:35','11:40 a 12:30','Almuerzo','2:00 a 2:50','2:55 a 3:45','3:50 a 4:40','4:45 a 5:35','5:40 a 6:30']
    seccionesReturn=[]
    profesores= []
    for i in muestra:
        profesoresTemp=[]
        seccionesReturn.append(seccionesFinal[i])
        horario_temp= [["" for x in range(12)] for x in range(6)]

        #AQui hago el formato basico de horarios;
        for hora in range(12):
                horario_temp[0][hora]= horas[hora]
        #Aqui Agrego las materias;
        for num in range(len(materiasCode)):
            profesoresTemp.append(PROFESORES[materiasCode[num]][seccionesFinal[i][num]])
            clases=MATERIAS[materiasCode[num]]['secciones'][seccionesFinal[i][num]]
            for elemento in clases:
                horario_temp[elemento[0]][elemento[1]-7]= MATERIAS[materiasCode[num]]['name']
        horario.append(comprimir(horario_temp))
        profesores.append(profesoresTemp)
    return [horario,cantidad,materiasName,seccionesReturn,profesores,len(materiasName)]

## comprime los horarios para luego se rendericen mejor
def comprimir(horario):
    final =[]
    for dia in horario:
        dia_act =[[dia[0],1]]
        p=0
        temp= dia[0]
        for i in range(1,len(dia)):
            if dia[i] == temp:
                dia_act[p][1]+=1
                dia_act.append(None)
            else:
                p=i
                temp=dia[i]
                dia_act.append([dia[i],1])
        final.append(dia_act)
    return final

# Retorna True si Ninguna choca o es valida
def check(lista):
    return len(lista)==len(set(lista)) and not "NoAplica" in lista

#print(MATERIAS['EB1134'])
#posibleHorario([], [['EB1134',1]])
#posibleHorario(['EB1134'])