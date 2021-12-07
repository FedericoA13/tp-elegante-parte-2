import constantes as const
import string
import random

def matriz_juego():
    #creo 1 matriz de numeros que es la que vera el usuario
    matriz_posiciones=[]
    FILAS_COMODIN=int(const.FILAS/const.FILAS) #Esto hace que se genere una sola linea que dps se cortara y stackeara 
    for i in range(FILAS_COMODIN):
        matriz_posiciones.append([])
        for j in range(1,const.FILAS*const.COLUMNAS+1):
            matriz_posiciones[i].append(j)
    
    #creo una matriz de letras aleatoria
    matriz_letras=[]
    matriz_letras_total=string.ascii_letters
    matriz_letras=random.sample(matriz_letras_total,int(const.FILAS*const.COLUMNAS/2))
    matriz_letras=(matriz_letras*2)
    random.shuffle(matriz_letras)
    
    #Agarro la linea de la matriz_posiciones y la la matriz_letra, las corto en partes = y las stackeo cada 1 en su matriz     
    if const.FILAS>1:
        matriz_posiciones_stackeada=[matriz_posiciones[0][x:x+const.VALOR] for x in range(0,len(matriz_posiciones[0]),const.VALOR)]
        matriz_letras_stackeada=[matriz_letras[x:x+const.VALOR] for x in range(0,len(matriz_letras),const.VALOR)]
    else:
        matriz_posiciones_stackeada=matriz_posiciones
        matriz_letras_stackeada=[matriz_letras]
#     print (matriz_posiciones_split)
#     print (matriz_letras_split)
        
    return matriz_posiciones_stackeada, matriz_letras_stackeada
    
def mostrar_fichas_posiciones(matriz_posiciones_stackeada,matriz_letras_stackeada):
    print("Fichas y Posiciones: ")
    for i in range(int(const.FILAS)):
        for j in range(int(const.COLUMNAS)):
            if len(str(matriz_posiciones_stackeada[i][j]))==1:
                print("[ ",str(matriz_posiciones_stackeada[i][j]),"]", end=" ")
            else:
                print("[",str(matriz_posiciones_stackeada[i][j]),"]", end=" ")
        print()
        
    return

def conversor_matriz(matriz):
#convierte 1 matriz con 1 sola fila en una matriz con varias filas que coinciden con el
#parametro FILAS seteado al principio. Y viciversa, convierte una matriz de varias filas en una
#de 1 sola fila
    if len(matriz)>1:
        matriz_nueva=[]
        for sublista in matriz:
            for item in sublista:
                matriz_nueva.append(item)
        matriz_nueva=[matriz_nueva]
    else:
        matriz_nueva=[matriz[0][x:x+const.VALOR] for x in range(0,len(matriz[0]),const.VALOR)]
        
    return matriz_nueva

def pedir_posiciones(matriz_posiciones_stackeada,contador_posicion):
    validacion_posicion=False
    matriz=conversor_matriz(matriz_posiciones_stackeada)
    
    # se validara que el numero ingresado sea un entero, este en las posiciones mostradas en la
    #pantalla y ademas no haya sido seleccionado antes
    while not validacion_posicion:
        try:
            if contador_posicion==1:
                posicion=int(input("Ingrese 1ra posicion: "))
            else:
                posicion=int(input("Ingrese 2da posicion: "))
            if 1<=posicion<=(int(const.FILAS*const.COLUMNAS)):
                if posicion in matriz[0]:
                    validacion_posicion=True
                else:
                    print("Ha ingresado un valor ya seleccionado antes. Vuelva a ingresar un valor")
                    validacion_posicion=False    
            else:
                print("Ha ingresado un valor fuera del rango permitido. Vuelva a ingresar un valor")
                validacion_posicion=False
        except:
            print("No has ingresado un valor numerico. Vuelve a ingresar un valor")
            validacion_posicion=False
            
    return posicion
        
def main():
    
    matriz_posiciones_stackeada, matriz_letras_stackeada=matriz_juego()
    mostrar_fichas_posiciones(matriz_posiciones_stackeada,matriz_letras_stackeada)
    
    letras_descubiertas=0
    intentos=0
    
    while letras_descubiertas<int(const.FILAS*const.COLUMNAS/2):
        contador_posicion=1
        posicion1=pedir_posiciones(matriz_posiciones_stackeada,contador_posicion)-1
        
        #convierto matriz mostrada en pantalla en matriz de 1 fila y asigno operaciones
        matriz_letras_stackeada=conversor_matriz(matriz_letras_stackeada)
        ficha1=matriz_letras_stackeada[0][posicion1]
        matriz_posiciones_stackeada=conversor_matriz(matriz_posiciones_stackeada)
        matriz_posiciones_stackeada[0][posicion1]=str(ficha1)
        
        #reconvierto matrices para volver a mostrar en pantalla
        matriz_letras_stackeada=conversor_matriz(matriz_letras_stackeada)
        matriz_posiciones_stackeada=conversor_matriz(matriz_posiciones_stackeada)
        mostrar_fichas_posiciones(matriz_posiciones_stackeada,matriz_letras_stackeada)
        
        contador_posicion=2
        posicion2=pedir_posiciones(matriz_posiciones_stackeada,contador_posicion)-1
        
        #convierto matriz mostrada en pantalla en matriz de 1 fila y asigno operaciones
        matriz_letras_stackeada=conversor_matriz(matriz_letras_stackeada)
        ficha2=matriz_letras_stackeada[0][posicion2]
        matriz_posiciones_stackeada=conversor_matriz(matriz_posiciones_stackeada)
        matriz_posiciones_stackeada[0][posicion2]=str(ficha2)
        
        #reconvierto matrices para volver a mostrar en pantalla
        matriz_letras_stackeada=conversor_matriz(matriz_letras_stackeada)
        matriz_posiciones_stackeada=conversor_matriz(matriz_posiciones_stackeada)
        mostrar_fichas_posiciones(matriz_posiciones_stackeada,matriz_letras_stackeada)
        
        #se crea lista que retorna a los valores originales las posiciones que el usuario pidio ver
        lista_validacion=[x for x in range(1,const.FILAS*const.COLUMNAS+1)]
        
        if ficha1!=ficha2:
            matriz_posiciones_stackeada=conversor_matriz(matriz_posiciones_stackeada)
            matriz_letras_stackeada=conversor_matriz(matriz_letras_stackeada)
            
            matriz_posiciones_stackeada[0][posicion1]=lista_validacion[posicion1]
            matriz_posiciones_stackeada[0][posicion2]=lista_validacion[posicion2]
            
            matriz_posiciones_stackeada=conversor_matriz(matriz_posiciones_stackeada)
            matriz_letras_stackeada=conversor_matriz(matriz_letras_stackeada)
            
            print("Las posiciones seleccionadas no tenian la misma letra. Vuelve a intentarlo")
            
            mostrar_fichas_posiciones(matriz_posiciones_stackeada,matriz_letras_stackeada)
            intentos=intentos+1
        else:
            print("Muy bien. Encontraste un par de letras iguales")
            letras_descubiertas=letras_descubiertas+1
            intentos=intentos+1
            
    print("Felicitaciones. Has encontrado todos los pares de letras. Has ganado.")
    print("Te ha llevado",intentos,"intentos resolver el memotest")
            
main()