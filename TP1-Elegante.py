import constantes as const
import string
import random
from timeit import default_timer
from tkinter import *
import math


def matriz_juego():
    """
    Autor: Fernando Michnowicz

    Esta función crea la matriz que figurará en pantalla para el juego del memotest,
    y crea otra matriz asociada a la misma compuesta con letras aleatoriamente
    distribuidas.
    """
    matriz_posiciones = []
    for i in range(1, int(const.FILAS * const.COLUMNAS + 1)):
        matriz_posiciones.append(i)

    matriz_letras = []
    matriz_letras_total = string.ascii_letters
    matriz_letras = random.sample(matriz_letras_total, int(const.FILAS * const.COLUMNAS / 2))
    matriz_letras = (matriz_letras * 2)
    random.shuffle(matriz_letras)

    matriz_posiciones_apiladas = [matriz_posiciones[x:x + const.VALOR] for x in
                                  range(0, len(matriz_posiciones), const.VALOR)]
    matriz_letras_apiladas = [matriz_letras[x:x + const.VALOR] for x in range(0, len(matriz_letras), const.VALOR)]

    return matriz_posiciones_apiladas, matriz_letras_apiladas


def mostrar_fichas_posiciones(matriz_posiciones_apiladas):
    """
    Autor: Federico Aldrighetti

    Esta función modifica la matriz creada para que se pueda imprimir en pantalla. En los
    números del 1 al 9, se agregará un espacio en la ficha para que el número quede bien
    alineado en la matriz.

    """
    print("Fichas y Posiciones: ")
    for i in range(int(const.FILAS)):
        for j in range(int(const.COLUMNAS)):
            if len(str(matriz_posiciones_apiladas[i][j])) == 1:
                print("[ ", str(matriz_posiciones_apiladas[i][j]), "]", end=" ")
            else:
                print("[", str(matriz_posiciones_apiladas[i][j]), "]", end=" ")
        print()

    return


def conversor_matriz(matriz):
    """
    Autor: Fernando Michnowicz

    Esta función convierte una lista con multiples listas en su interior en una lista con 1 sola lista
    en su interior y viciversa. El objetivo es facilitar operaciones de validacion, busqueda de posiciones y
    reemplazo por letras y/o numeros en la matriz que el usuario ve en pantalla a medida que escoge posiciones.
    """

    if len(matriz) > 1:
        matriz_nueva = []
        for sublista in matriz:
            for item in sublista:
                matriz_nueva.append(item)
        matriz_nueva = [matriz_nueva]
    else:
        matriz_nueva = [matriz[0][x:x + const.VALOR] for x in range(0, len(matriz[0]), const.VALOR)]

    return matriz_nueva


def pedir_validar_posiciones(matriz_posiciones_apiladas, contador_posicion):
    """
    Autor: Federico Aldrighetti

    Esta función valida los ingresos de los jugadores, avisa cuando un input
    no es válido y en este caso, solicita que se vuelva a ingresar
    """
    validacion_posicion = False
    matriz_a_chequear = conversor_matriz(matriz_posiciones_apiladas)

    while not validacion_posicion:
        try:
            if contador_posicion == 1:
                posicion = int(input("Ingrese 1ra posicion: "))
            else:
                posicion = int(input("Ingrese 2da posicion: "))
            if 1 <= posicion <= (int(const.FILAS * const.COLUMNAS)):
                if posicion in matriz_a_chequear[0]:
                    validacion_posicion = True
                else:
                    print("Ingresaste un valor ya seleccionado antes. Volve a ingresar otro valor")
                    validacion_posicion = False
            else:
                print(
                    "Ingresaste un valor fuera del rango permitido. Solo podés ingresar los valores que ves en pantalla. Volvé a ingresar otro valor")
                validacion_posicion = False
        except:
            print(
                "Ingresaste un valor o caracter no permitido. Solo podés ingresar los valores que ves en pantalla. Volvé a ingresar otro valor")
            validacion_posicion = False

    return posicion


def buscar_reemplazar_posiciones(matriz_posiciones_apiladas, matriz_letras_apiladas, posicion):
    """
    Autores: Lautaro López y Germán Seckar

    Esta función reemplaza el valor que se ve en la pantalla de la posición con la letra que está oculta en esa misma posición.
    Convierte las matrices de posiciones y letras en matrices de una sola fila para facilitar operaciones de buscar y encontrar fichas.
    """

    matriz_letras_apiladas = conversor_matriz(matriz_letras_apiladas)
    ficha = matriz_letras_apiladas[0][posicion]
    matriz_posiciones_apiladas = conversor_matriz(matriz_posiciones_apiladas)
    matriz_posiciones_apiladas[0][posicion] = str(ficha)

    matriz_letras_apiladas = conversor_matriz(matriz_letras_apiladas)
    matriz_posiciones_apiladas = conversor_matriz(matriz_posiciones_apiladas)

    return ficha, matriz_posiciones_apiladas, matriz_letras_apiladas


def resetear_matriz_posiciones(matriz_posiciones_apiladas, matriz_letras_apiladas, posicion1, posicion2):
    """
    Autor: Germán Seckar

    Si el jugador no acierta la letra con las fichas escogidas, esta función resetea los valores de la matriz de posiciones
    a la posicion que ocupaba la letra (es la inversa de la función buscar_reemplazar_posiciones). También crea una lista
    con números que son los que van a reemplazar a las letras (notar que tiene el mismo orden que la matriz_posiciones_apiladas).

    """

    lista_validacion = [x for x in range(1, int(const.FILAS * const.COLUMNAS + 1))]

    matriz_posiciones_apiladas = conversor_matriz(matriz_posiciones_apiladas)
    matriz_letras_apiladas = conversor_matriz(matriz_letras_apiladas)

    matriz_posiciones_apiladas[0][posicion1] = lista_validacion[posicion1]
    matriz_posiciones_apiladas[0][posicion2] = lista_validacion[posicion2]

    matriz_posiciones_apiladas = conversor_matriz(matriz_posiciones_apiladas)
    matriz_letras_apiladas = conversor_matriz(matriz_letras_apiladas)

    return matriz_posiciones_apiladas, matriz_letras_apiladas


def ganador_memotest(jugador_shuffle_1, jugador_shuffle_2, intentos_jugador_shuffle_1, intentos_jugador_shuffle_2,
                     letras_descubiertas_jugador_shuffle_1, letras_descubiertas_jugador_shuffle_2, matriz_jugadores):
    """
    Autor: Pablo González

    Esta función devuelve al ganador del juego si es que hubo uno, o muestra empate. En el caso de que
    los dos jugadores hayan encontrado la misma cantidad de fichas, el ganador será el que menos intentos
    haya necesitado.
    """

    if letras_descubiertas_jugador_shuffle_1 > letras_descubiertas_jugador_shuffle_2:
        resultado = print("El ganador de la partida es {} con {} pares de fichas encontradas".format(
            matriz_jugadores[jugador_shuffle_1], letras_descubiertas_jugador_shuffle_1))
    elif letras_descubiertas_jugador_shuffle_1 < letras_descubiertas_jugador_shuffle_2:
        resultado = print("El ganador de la partida es {} con {} pares de fichas encontradas".format(
            matriz_jugadores[jugador_shuffle_2], letras_descubiertas_jugador_shuffle_2))
    else:
        if intentos_jugador_shuffle_1 < intentos_jugador_shuffle_2:
            resultado = print(
                "El ganador de la partida es {}. Ambos encontraron {} pares de fichas pero {} lo hizo en menos intentos".format(
                    matriz_jugadores[jugador_shuffle_1], letras_descubiertas_jugador_shuffle_1,
                    matriz_jugadores[jugador_shuffle_1]))
        elif intentos_jugador_shuffle_1 > intentos_jugador_shuffle_2:
            resultado = print(
                "El ganador de la partida es {}. Ambos encontraron {} pares de fichas pero {} lo hizo en menos intentos".format(
                    matriz_jugadores[jugador_shuffle_2], letras_descubiertas_jugador_shuffle_2,
                    matriz_jugadores[jugador_shuffle_2]))
        else:
            resultado = print("Ha ocurrido un empate. Ambos encontraron {} pares de fichas en {} intentos".format(
                letras_descubiertas_jugador_shuffle_1, intentos_jugador_shuffle_1))

    return resultado


def tiempo_total(tiempo_inicial, tiempo_final):
    """
    Autor: Lautaro López

    Esta función pasa de segundos a minutos, si lo requiere.
    """

    minutos = math.floor((tiempo_final - tiempo_inicial) / 60)
    segundos = math.floor(
        ((tiempo_final - tiempo_inicial) / 60 - math.floor((tiempo_final - tiempo_inicial) / 60)) * 60)
    if tiempo_final - tiempo_inicial < 60:
        print(f"Felicitaciones. El juego ha terminado. La partida duró {segundos} segundos")
    elif int(minutos) == 1 and not int(segundos) == 1:
        print(f"Felicitaciones. El juego ha terminado. La partida duró {minutos} minuto con {segundos} segundos")
    elif int(minutos) == 1 and int(segundos) == 1:
        print(f"Felicitaciones. El juego ha terminado. La partida duró {minutos} minuto con {segundos} segundo")
    else:
        print(f"Felicitaciones. El juego ha terminado. La partida duró {minutos} minutos con {segundos} segundos")


def interfaz_grafica():
    """
    Autor: Pablo González

    Esta función configura la interfaz gráfica que aparecerá cuando se pida los nombres de los jugadores.
    """

    ventana = Tk()
    ventana.title("Memotest - Ingreso de nombres")
    ventana.geometry("400x170")
    ventana.resizable(0, 0)
    ventana.config(bg="black")

    miframe = Frame()
    miframe.pack()

    miframe.config(bg="lightblue")
    miframe.config(width="350", height="170")
    miframe.config(bd=10)
    miframe.config(relief="sunken")

    etiqueta_bievenidos = Label(miframe, text="Bienvenidos al juego del memotest").place(x=75, y=10)
    etiqueta_jugador1 = Label(miframe, text="Ingrese nombre Jugador 1").place(x=30, y=45)
    etiqueta_jugador2 = Label(miframe, text="Ingrese nombre Jugador 2").place(x=30, y=75)

    def codigo_boton():
        if jugador_1.get() == "" or jugador_2.get() == "":
            messagebox.showinfo("Atención", "Por favor, tenés que nombrar a los 2 jugadores")
        else:
            ventana.destroy()

    jugador_1 = StringVar()
    jugador_2 = StringVar()

    cuadro_jugador_1 = Entry(miframe, textvariable=jugador_1).place(x=180, y=45)
    cuadro_jugador_2 = Entry(miframe, textvariable=jugador_2).place(x=180, y=75)

    boton_comenzar_juego = Button(miframe, text="Comenzar a jugar", command=codigo_boton).place(x=125, y=110)

    ventana.mainloop()

    matriz_jugadores = [jugador_1.get(), jugador_2.get()]

    return matriz_jugadores


def main():
    """
    Autor: en conjunto

    En esta función se inicia el juego, se llama a las demás funciones que forman el programa
    y da información sobre la partida, desde que se inicia hasta su fin.
    """

    tiempo_inicial = default_timer()
    matriz_jugadores = interfaz_grafica()  # la matriz de jugadores proviene de la interfaz grafica de tkinter
    random.shuffle(matriz_jugadores)
    turno_jugador_shuffle = matriz_jugadores[0]

    print("Comenzará jugando:", turno_jugador_shuffle)

    matriz_posiciones_apiladas, matriz_letras_apiladas = matriz_juego()
    mostrar_fichas_posiciones(matriz_posiciones_apiladas)

    letras_descubiertas = 0  # contador de letras descubiertas
    intentos_jugador_shuffle_1 = 0  # contador intentos del jugador 1 de la matriz mezclada
    intentos_jugador_shuffle_2 = 0  # contador intentos del jugador 2 de la matriz mezclada
    letras_descubiertas_jugador_shuffle_1 = 0  # contador letras descubiertas del jugador 1 de la matriz mezclada
    letras_descubiertas_jugador_shuffle_2 = 0  # contador letras descubiertas del jugador 2 de la matriz mezclada
    jugador_shuffle_1 = 0  # posicion que ocupa el jugador 1 en la matriz_jugadores mezclada
    jugador_shuffle_2 = 1  # posicion que ocupa el jugador 1 en la matriz_jugadores mezclada

    while letras_descubiertas < int(const.FILAS * const.COLUMNAS / 2):
        contador_posicion = 1
        posicion1 = pedir_validar_posiciones(matriz_posiciones_apiladas, contador_posicion) - 1
        ficha1, matriz_posiciones_apiladas, matriz_letras_apiladas = buscar_reemplazar_posiciones(
            matriz_posiciones_apiladas, matriz_letras_apiladas, posicion1)
        mostrar_fichas_posiciones(matriz_posiciones_apiladas)

        contador_posicion = 2
        posicion2 = pedir_validar_posiciones(matriz_posiciones_apiladas, contador_posicion) - 1
        ficha2, matriz_posiciones_apiladas, matriz_letras_apiladas = buscar_reemplazar_posiciones(
            matriz_posiciones_apiladas, matriz_letras_apiladas, posicion2)
        mostrar_fichas_posiciones(matriz_posiciones_apiladas)

        if ficha1 != ficha2:
            matriz_posiciones_apiladas, matriz_letras_apiladas = resetear_matriz_posiciones(matriz_posiciones_apiladas,
                                                                                            matriz_letras_apiladas,
                                                                                            posicion1, posicion2)

            if turno_jugador_shuffle == matriz_jugadores[jugador_shuffle_1]:
                intentos_jugador_shuffle_1 += 1
                print("Mala suerte", matriz_jugadores[jugador_shuffle_1],
                      "las posiciones seleccionadas no tenian la misma letra. Le toca jugar a",
                      matriz_jugadores[jugador_shuffle_2])
                turno_jugador_shuffle = matriz_jugadores[jugador_shuffle_2]
            else:
                intentos_jugador_shuffle_2 += 1
                print("Mala suerte", matriz_jugadores[jugador_shuffle_2],
                      "las posiciones seleccionadas no tenian la misma letra. Le toca jugar a",
                      matriz_jugadores[jugador_shuffle_1])
                turno_jugador_shuffle = matriz_jugadores[jugador_shuffle_1]

            mostrar_fichas_posiciones(matriz_posiciones_apiladas)
        else:
            letras_descubiertas += 1
            if letras_descubiertas < int(const.FILAS * const.COLUMNAS / 2):
                if turno_jugador_shuffle == matriz_jugadores[jugador_shuffle_1]:
                    intentos_jugador_shuffle_1 += 1
                    letras_descubiertas_jugador_shuffle_1 += 1
                    print("Muy bien", matriz_jugadores[jugador_shuffle_1],
                          "encontraste un par de letras iguales. Puedes continuar jugando")
                else:
                    intentos_jugador_shuffle_2 += 1
                    letras_descubiertas_jugador_shuffle_2 += 1
                    print("Muy bien", matriz_jugadores[jugador_shuffle_2],
                          "encontraste un par de letras iguales. Puedes continuar jugando")
            else:
                if turno_jugador_shuffle == matriz_jugadores[jugador_shuffle_1]:
                    intentos_jugador_shuffle_1 += 1
                    letras_descubiertas_jugador_shuffle_1 += 1
                    print("Muy bien", matriz_jugadores[jugador_shuffle_1],
                          "encontraste un par de letras iguales. Ya no quedan más letras por encontrar")
                else:
                    intentos_jugador_shuffle_2 += 1
                    letras_descubiertas_jugador_shuffle_2 += 1
                    print("Muy bien", matriz_jugadores[jugador_shuffle_2],
                          "encontraste un par de letras iguales. Ya no quedan más letras por encontrar")

    tiempo_final = default_timer()

    tiempo_total(tiempo_inicial, tiempo_final)

    ganador_memotest(jugador_shuffle_1, jugador_shuffle_2, intentos_jugador_shuffle_1, intentos_jugador_shuffle_2,
                     letras_descubiertas_jugador_shuffle_1, letras_descubiertas_jugador_shuffle_2, matriz_jugadores)


main()