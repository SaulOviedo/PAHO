import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
camino = os.path.join(__location__,"horario.txt")
#camino = "horario.txt"
arch= open(camino, 'r', encoding='utf8')

##Variables funcionales para codigo
MATERIAS = {}
PROFESORES = {}
CAREERS = {}
nombreTemp = []
Banderin = False
##lo que entregara al dict
nombre=""
code=""
career=""
seccion=0
horario=[]
##El superior mantiene registro si la linea anterior fue solo texto

def profesor(linea):
    k=-1
    if not linea[k].isalpha():
        return ""
    while not linea[k-1].isdigit():
        k-=1
    k+=1
    return ' '.join(linea[k:])

def isalphaArray(lista):
    for palabra in lista:
        if not palabra.isalpha():
            return False
    return True

def completar():
    for c in MATERIAS.keys():
            mayor = max(MATERIAS[c]['secciones'].keys())
            for i in range(1,mayor):
                if not i in MATERIAS[c]['secciones'].keys():
                    MATERIAS[c]['secciones'].update({i:["NoAplica"]})

for line in arch:
    ##Aqui se actualiza las horas de clases
    clasesTemp= []
    linea = line
    linea = linea.replace('.',' ').replace(',',' ')
    linea = linea.split()
    if len(linea) !=0 and linea[0] == '---':
        career = linea[1:]
    else:
        ## si la linea es solo texto, lo guardaremos para despues.
        if isalphaArray(linea):
            nombreTemp= linea
            Banderin = True
        elif Banderin:
            i=0
            while linea[i].isalpha():
                i+=1
            nombreTemp = nombreTemp + linea[0:i]
            code=linea[i]
            secc=linea[i+1]

            if( not linea[i+4].isdigit()):
                j=i+2
            else:
                j=i+3

            while linea[j].isdigit() and linea[j+1].isdigit():
                if int(linea[j]) not in range(6) or int(linea[j+1]) not in range(7,19):
                    print("error; si encuentras esto deberias revisar  Cerca del Texto. Iniciador, existe una meteria q no tiene el horario bien",int(linea[j]),int(linea[j+1]), nombre, seccion, clasesTemp)
                clasesTemp.append((int(linea[j]),int(linea[j+1])))
                if j+5 <= len(linea):
                    j+=3
                else:
                    break

            nombre=' '.join(nombreTemp)
            seccion=int(secc)
            horario=clasesTemp

            Banderin = False

        else:
            i=0
            while linea[i].isalpha():
                i+=1
            nombreTemp = linea[0:i]
            code= linea[i]
            secc=linea[i+1]

            if( not linea[i+4].isdigit()):
                j=i+2
            else:
                j=i+3

            while linea[j].isdigit() and linea[j+1].isdigit():
                clasesTemp.append((int(linea[j]),int(linea[j+1])))
                if j+5 <= len(linea):
                    j+=3
                else:
                    break


            nombre=' '.join(nombreTemp)
            seccion=int(secc)
            horario=clasesTemp

        if not Banderin:
            if code in MATERIAS.keys():
                MATERIAS[code]['secciones'].update({seccion:horario})
                PROFESORES[code].update({seccion:profesor(linea)})
                if CAREERS[code] != career: print("Codigo repetido: " + code)
            else:
                MATERIAS.update({code:{'name': nombre, 'secciones':{seccion:horario}}})
                PROFESORES.update({code:{seccion:profesor(linea)}})
                CAREERS.update({code: career})
completar()
arch.close()

#print('---------------------------------------------------------------')
#print([MATERIAS[code]['name'] for code in MATERIAS])
#print('---------------------------------------------------------------')
#print(MATERIAS)
#print('---------------------------------------------------------------')
#print(len(MATERIAS.keys()))
#print('---------------------------------------------------------------')
#print(PROFESORES)
#print(CAREERS)

