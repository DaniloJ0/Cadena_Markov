#palabra="abbbcabcbbbcb"  
# k=2 ab bb bb bc ca ab bc cb bb bb bc cb
# k=3 abb bbb bba bbc bca cab abc bcb cbb bbb bbc [bcb] 
# k=4 abbb bbbc bbca bcab cabc abcb bcbb cbbb bbbc [bbcb] 
import numpy as np, random
import matplotlib.pyplot as plot
import seaborn as sb
reset=0
while reset==0:
    caracteres={}
    probabilidades={}
    filename= 'Ejemplo.txt'
    palabra=""
    with open(filename) as f_obj:
        for line in f_obj:
            palabra= palabra+line.rstrip()
    n=len(palabra)
    f = open ("Result.txt", "w") #Aquí "Formateo" el archivo Result.txt para hacer prueba con el mismo ejemplo"
    f.write(palabra)
    f.close()
    K=int(input("Ingresa el valor de K: "))
    N=int(input("Ingresa el valor de N: "))
    i=0
    while i <= n and i+K<n: # Va de 0 a 13
        cadena=palabra[i:i+K]
        aux=[]
        if caracteres: #si el diccionario no está vacío
            if cadena in caracteres: #Si la cadena ya existe en el diccionario
                    aux=caracteres[cadena]
                    aux[0]=aux[0]+1
                    aux.append(palabra[i+K])
                    caracteres[cadena]=aux
            else:
                    caracteres[cadena]=[1,palabra[i+K]]  #Se agrega la cadena sino existe
        else: # Cuando el diccionario se encuentre vacío
            caracteres[cadena]=[1,palabra[i+K]] # [Cuantas veces se repite la cadena, letra que le sigue]
        i+=1

    #Aquí vamos a guardar las probabilidades de cada letra en tupla dentro de una lista
    for clave,valor  in caracteres.items():
        ListaTupla=[]
        #u=Array normal sin repetidos
        #indx=Array con las veces repetida cada letra
        u,indx = np.unique(valor,return_counts = True) # Saco cuantas veces se repite las letras
        for i in range(1,len(indx)):
            #Numero de veces que se repite entre el numero total de caracteres
            prob=indx[i]/valor[0] 
            ListaTupla.append((u[i],round(prob, 2)))  #Guarda una tupla en una lista con los valores de las probaablidades de cada letra
        probabilidades[clave]=ListaTupla

    #Desde esta parte se Genera el Texto
    def caracter(valor, listproba): #Esta función me ayuda a buscar los cararecteres segun su probabilidad (Cuando son iguales), lo guarda en una lista y luego lo ordena
        rep=[]
        for i in range(0,len(listproba)):
            if listproba[i][1]==valor:
                rep.append(listproba[i][0])
        rep.sort() 
        return rep[0]

    for i in range(0,N):
        filename= 'Result.txt'
        word=""
        with open(filename) as f_obj: #Lee el archivo donde se esta escribiendo el resultado
            for line in f_obj:
                word= word+line.rstrip()
        listproba=[]
        limit=len(word)
        start= word[limit-K:limit] #Tomo la K-tuplas finales
        listproba=probabilidades[start]
        numRandom=round(random.random(),2)
        max1=""
        lis=[]
        for i in range(0,len(listproba)): #Aquí guardo todas las probabilidades de las letra de cada clave para así tener un buen manejo de ellas
            lis.append(listproba[i][1])
        lis.sort()
        sw=0
        h=0
        na=len(lis)
        while sw==0 and h<na: #En este Ciclo determino qué letra irá después según el valor del random
            if lis[h]>= numRandom:
                sw=1
                indx=h
                j=h
                if h+1<na:
                    while  j<na and lis[h+1] == lis[indx]:
                        j+=1
                max1=caracter(lis[indx],listproba)
            else: #Este es el caso para cuando el random sea mayor que la ultimo probabilidad
                if h==na-1:   # and na-1 !=0
                    sw=1
                    indx=h
                    j=na
                    while j>0 and lis[h-1] == lis[indx]: #En este Ciclo 
                        j-=1
                    max1=caracter(lis[indx],listproba)        
            h+=1 
        f = open ("Result.txt", "a")
        f.write(max1)
        f.close()
    def ContenidoArchivo(filename):
        word=""
        with open(filename) as f_obj: #Lee el archivo donde se está escribiendo el resultado
            for line in f_obj:
                word= word+line.rstrip()
        return word
    menu = """
    Menú
    1- Generar texto
    2- Mostrar histograma
    3- Intentar de nuevo
    4- Salir
    """
    sw=True
    while sw==True:
        print(menu)
        op=int(input("Seleccione una opción: "))
        if op == 1:
            filename= 'Result.txt'
            word=ContenidoArchivo(filename)
            print("El texto generado es: ",word)
        else:
            if op == 2:
                lista=[]
                word=ContenidoArchivo("Result.txt")
                n=len(word)
                while i <= n and i+K<n: # Va de 0 a 13
                    cade=word[i:i+K]
                    lista.append(cade)
                    i+=1
                intervalos = len(lista) #calculamos los extremos de los intervalos
                sb.displot(lista, color='#F2AB6D', bins=intervalos, kde=True) #creamos el gráfico en Seaborn
                #plot.xticks(rangos)
                plot.ylabel('Frecuencia')
                plot.xlabel('Caracteres')
                plot.title('Histograma de caracteres')
                plot.show()
            else:
                if op==3:
                    sw=False
                    archivo=open("Result.txt","w")
                    archivo.write(palabra)
                    archivo.close()
                else:   
                    reset=1
                    sw=False

#Arreglar el código para validar que las probabilidades iguales varien en su elección
