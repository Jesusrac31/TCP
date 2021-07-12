import numpy as np #Importamos matrices
import random #Importamos números aleatorios

class Grafo(): #Creamos la clase de los vectores
    def __init__(self,nodos): #Fijamos parametros principales

        self.nodos = nodos #Volvemos el número de nodos una variable global en la clase
        self.nodos_debug = 5
        self.vector = np.zeros((nodos,nodos)) #Creamos una matriz cuadrada con todos los valores en 0 coincidiendo el número de nodos y el tamaño de las filas y columnas. Esta sera una matriz de adyascencias

        self.vector_debug = np.array([[0,10,-1,30,100],
                                       [10,0,50,-1,-1],
                                       [-1,50,0,20,10],
                                       [30,-1,20,0,60],
                                       [100,-1,10,60,0]]) #Creamos una matriz para debug

        self.dist_min=0
        self.camino_min=[]

    def imprimir(self): #Creamos una función que imprima la matriz

        print(self.vector) #Imprimimos la matriz
    
    def imprimir_debug(self): #Creamos una función que imprima la matriz debug

        print(self.vector_debug) #Imprimimos la matriz debug

    def fijar_valores(self): #Creamos la clase para fijar valores
        for i in range(self.nodos): #Recorremos la matriz
            for j in range(self.nodos):
                if j != i and self.vector[i,j] == 0: #Comprobamos si es una de la diagonal o ya se ha rellenado
                    cero = True 
                    while cero: #Hacemos un bucle
                        dist = int(input('Distancia entre el nodo '+str(i+1)+' y el '+str(j+1)+' (si no estan conectados escribe -1) ')) #Le preguntamos la distancia entre 2 vectores
                        if dist != 0: #Si la respuesta no es 0
                            cero = False #Paramos el bucle
                            self.vector[i,j] = dist #Fijamos la distancia entre estos 2 a la matriz
                            self.vector[j,i] = dist #Como es un esquema sin direcciones es una matriz simetrica, por lo que la fijamos a la de la posición opuesta
                        else: #Si la respuesta es 0
                            print()
                            print('La distancia entre 2 nodos no puede ser 0') # Decimos que es imposible y como no hemos quitado el bucle volveremos a preguntar
                            print()
    
    def texto(self): #Función que pasa de txt a matriz

        f = open ('matriz.txt','r') #Abrimos el archivo de texto
        mensaje = f.read() #Coje lo que contiene el archivo
        f.close() #Cerramos el archivo
        activa='' #Variable en la que iremos almacenando cada división poco a poco
        filas=[] #Lista en la que se almacena las divisiones
        for i in mensaje: #Por cada letra del mensaje
            if i != '\n': #Si no hay un enter
                activa = activa+i #Archivamos letras
            if i == ']': #Las divisiones estan hechas con ] por lo que si estamos en ese caracter
                filas.append(activa) #Metemos la división en la lista
                activa='' #Reseteamos la variable de almacenamiento

        x=0 #Fijamos las variables que diran la posición de la matriz en la que estamos
        y=0
        for j in filas: #Recorremos la lista
            for i in j: #Por cada letra de la división
                if i == ',' or i == ']': #Miramos si hay alguna división
                    self.vector[x,y]=int(activa) #Meteriamos la división en la matriz
                    y+=1 #Pasariamos a la siguiente casilla
                    if y>self.nodos-1:
                        y=0
                        x+=1
                    activa='' #Reseteamos la variable de almacenamiento
                elif i != '[': #Saltamos el caracte [
                    activa = activa+i

    def generar_vector(self):

        file = open("matriz.txt", "w") #Abrimos o creamos el archivo matriz.txt
        matrizG = np.zeros((self.nodos,self.nodos)) #Creamos una matriz
        for i in range(self.nodos): #Durante todos los nodos
            for j in range(self.nodos): #En fila y columnas
                if matrizG[i,j] == 0 and j!= i: #Si no se ha puesto ningún número
                    matrizG[i,j] = str(random.randint(20,200)) #Sera un número aleatorio entre 20 y 200
                    matrizG[j,i] = matrizG[i,j] #En el opuesto tambien ya que es simétrica

        #La escribimos

        for i in matrizG: 
            file.write('[')
            for x,j in enumerate(i):
                if x != 0:
                    file.write(',')
                file.write(str(int(j)))

            file.write(']\n') #Esto pone un ] y un enter
        file.close()
    
    def TSP(self,inicio):

        self.camino_min=[]
        self.dist_min=-1
        camino = []
        for i in range(self.nodos-1):
            camino.append(0)
        while camino[0] != self.nodos:
            poder = True
            for x,i in enumerate(camino):
                for y,j in enumerate(camino):
                    if i==j and x != y or j == inicio:
                        poder = False
            if poder:
                self.comprobamos(inicio,camino)
            camino[-1]+=1
            for i in range(len(camino)):
                if camino[len(camino)-i-1]==self.nodos:
                    if len(camino)-i-1 != 0:
                        camino[len(camino)-i-1]=0
                        camino[len(camino)-i-2]+=1
        print(self.camino_min)
        print(self.dist_min)

    def comprobamos(self,inicio,camino):

        camino_completo=camino.copy()
        camino_completo.append(inicio)
        camino_completo.insert(0,inicio)
        dist=0
        for i in range(len(camino_completo)-1):
            dist+= self.vector[camino_completo[i],camino_completo[i+1]]
        if dist<self.dist_min or self.dist_min==-1:
            self.camino_min=camino_completo.copy()
            self.dist_min=dist

vectores=Grafo(int(input('Número de nodos: '))) #Iniciamos la clase preguntando el número de nodos

vectores.generar_vector()
vectores.texto() #Lee el texto
vectores.imprimir() #Imprimimos la matriz
inicio = int(input('Punto de partida: '))
vectores.TSP(inicio-1)