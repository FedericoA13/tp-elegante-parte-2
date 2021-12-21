import string
import random
from timeit import default_timer
from tkinter import *
import math
import time
import csv

### CONSTANTES ###
JugadorTurno=0
JugadorSiguiente=1
aciertos=0
intentos=1
promedio=2


partida=1


def matriz_juego(FILAS, COLUMNAS, VALOR):
    """
    Autor: Fernando Michnowicz

    Esta función crea la matriz que figurará en pantalla para el juego del memotest,
    y crea otra matriz asociada a la misma compuesta con letras aleatoriamente
    distribuidas.
    """
    matriz_posiciones = []
    for i in range(1, int(FILAS * COLUMNAS + 1)):
        matriz_posiciones.append(i)

    matriz_letras = []
    matriz_letras_total = string.ascii_letters
    matriz_letras = random.sample(matriz_letras_total, int(FILAS * COLUMNAS / 2))
    matriz_letras = (matriz_letras * 2)
    random.shuffle(matriz_letras)

    matriz_posiciones_apiladas = [matriz_posiciones[x:x + VALOR] for x in
                                  range(0, len(matriz_posiciones), VALOR)]
    matriz_letras_apiladas = [matriz_letras[x:x + VALOR] for x in range(0, len(matriz_letras), VALOR)]

    return matriz_posiciones_apiladas, matriz_letras_apiladas


def mostrar_fichas_posiciones(matriz_posiciones_apiladas, FILAS, COLUMNAS):
    """
    Autor: Federico Aldrighetti

    Esta función modifica la matriz creada para que se pueda imprimir en pantalla. En los
    números del 1 al 9, se agregará un espacio en la ficha para que el número quede bien
    alineado en la matriz.

    """
    print("Fichas y Posiciones: ")
    for i in range(int(FILAS)):
        for j in range(int(COLUMNAS)):
            if len(str(matriz_posiciones_apiladas[i][j])) == 1:
                print("[ ", str(matriz_posiciones_apiladas[i][j]), "]", end=" ")
            else:
                print("[", str(matriz_posiciones_apiladas[i][j]), "]", end=" ")
        print()

    return


def conversor_matriz(matriz, VALOR):
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
        matriz_nueva = [matriz[0][x:x + VALOR] for x in range(0, len(matriz[0]), VALOR)]

    return matriz_nueva


def pedir_validar_posiciones(matriz_posiciones_apiladas, contador_posicion, FILAS, COLUMNAS, VALOR):
    """
    Autor: Federico Aldrighetti

    Esta función valida los ingresos de los jugadores, avisa cuando un input
    no es válido y en este caso, solicita que se vuelva a ingresar
    """
    validacion_posicion = False
    matriz_a_chequear = conversor_matriz(matriz_posiciones_apiladas, VALOR)

    while not validacion_posicion:
        try:
            if contador_posicion == 1:
                posicion = int(input("Ingrese 1ra posicion: "))
            else:
                posicion = int(input("Ingrese 2da posicion: "))
            if 1 <= posicion <= (int(FILAS * COLUMNAS)):
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


def buscar_reemplazar_posiciones(matriz_posiciones_apiladas, matriz_letras_apiladas, posicion, VALOR):
    """
    Autores: Lautaro López y Germán Seckar

    Esta función reemplaza el valor que se ve en la pantalla de la posición con la letra que está oculta en esa misma posición.
    Convierte las matrices de posiciones y letras en matrices de una sola fila para facilitar operaciones de buscar y encontrar fichas.
    """

    matriz_letras_apiladas = conversor_matriz(matriz_letras_apiladas, VALOR)
    ficha = matriz_letras_apiladas[0][posicion]
    matriz_posiciones_apiladas = conversor_matriz(matriz_posiciones_apiladas, VALOR)
    matriz_posiciones_apiladas[0][posicion] = str(ficha)

    matriz_letras_apiladas = conversor_matriz(matriz_letras_apiladas, VALOR)
    matriz_posiciones_apiladas = conversor_matriz(matriz_posiciones_apiladas, VALOR)

    return ficha, matriz_posiciones_apiladas, matriz_letras_apiladas


def resetear_matriz_posiciones(matriz_posiciones_apiladas, matriz_letras_apiladas, posicion1, posicion2, FILAS, COLUMNAS, VALOR):
    """
    Autor: Germán Seckar

    Si el jugador no acierta la letra con las fichas escogidas, esta función resetea los valores de la matriz de posiciones
    a la posicion que ocupaba la letra (es la inversa de la función buscar_reemplazar_posiciones). También crea una lista
    con números que son los que van a reemplazar a las letras (notar que tiene el mismo orden que la matriz_posiciones_apiladas).

    """

    lista_validacion = [x for x in range(1, int(FILAS * COLUMNAS + 1))]

    matriz_posiciones_apiladas = conversor_matriz(matriz_posiciones_apiladas, VALOR)
    matriz_letras_apiladas = conversor_matriz(matriz_letras_apiladas, VALOR)

    matriz_posiciones_apiladas[0][posicion1] = lista_validacion[posicion1]
    matriz_posiciones_apiladas[0][posicion2] = lista_validacion[posicion2]

    matriz_posiciones_apiladas = conversor_matriz(matriz_posiciones_apiladas, VALOR)
    matriz_letras_apiladas = conversor_matriz(matriz_letras_apiladas, VALOR)

    return matriz_posiciones_apiladas, matriz_letras_apiladas


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
        
def validar_nombre(nombre):
    #Valida usuario
    valido = True
    letra = 0
    if 4 <= len(nombre) <= 15:
        while valido and not letra == len(nombre):
            if nombre[letra] == "_":
                valido = True
                letra += 1
            elif nombre[letra].isalnum():
                valido = True
                letra += 1
            else:
                valido = False
    else:
        valido = False
        
    return valido

def validar_contrasenia(contrasenia):
    #Valida contraseña
    letras_acentuadas = ["á","é","í","ó","ú"]
    letras_acentuadas_mayus = ["Á","É","Í","Ó","Ú"]
    contrasenia_guion = 0
    contrasenia_mayus = 0
    contrasenia_minus = 0
    contrasenia_numero = 0
    valido = True
    letra = 0
    
    if 8 <= len(contrasenia) <= 12:
        while valido and not letra == len(contrasenia):
            if contrasenia[letra] in letras_acentuadas or contrasenia[letra] in letras_acentuadas_mayus:
                valido = False
            else:
                if contrasenia[letra] == "_" or contrasenia[letra] == "-":
                    contrasenia_guion += 1
                    letra += 1
                elif contrasenia[letra].isupper():
                    contrasenia_mayus += 1
                    letra += 1
                elif contrasenia[letra].islower():
                    contrasenia_minus += 1
                    letra += 1
                elif contrasenia[letra].isnumeric():
                    contrasenia_numero += 1
                    letra += 1
                else:
                    valido = False
        if contrasenia_guion == 0 or contrasenia_mayus == 0 or contrasenia_minus == 0 or contrasenia_numero == 0:
            valido = False
    else:
        valido = False
    
    return valido

def contrasenia_igual(contrasenia, contrasenia2):
    #Compara contraseñas
    valido = False
    if contrasenia == contrasenia2:
        valido = True
    return valido

def agregar_a_archivos(nombre, contrasenia, preguntaseguridad):
    #Abre archivo usuarios.csv y escribe nombre y contraseñas si son correctos
    with open("usuarios.csv", "a", newline = "") as usuarios_archivo:
        usuarios_actualizado = csv.writer(usuarios_archivo, dialect = 'excel', delimiter = ";")
        usuarios_actualizado.writerows([[nombre, contrasenia, preguntaseguridad]])
        
        return
    
def crear_diccionario(lista):
    diccionario={}
    for nombre in lista:
        if not nombre in diccionario:
            diccionario[nombre]=[0,0,0]
        
    return diccionario

def ordenar_diccionario(diccionario):
    diccionario=dict(sorted(diccionario.items(), key=lambda item:item[1][0],reverse=True))
    return diccionario

def modificar_diccionario_intentos(nombre,diccionario):
    if nombre in diccionario:
        diccionario[nombre][1]+=1
    return diccionario

def modificar_diccionario_aciertos(nombre,diccionario):
    if nombre in diccionario:
        diccionario[nombre][0]+=1
        diccionario[nombre][1]+=1
    return diccionario

def modificar_diccionario_promedio(diccionario,contador):
    for nombre in diccionario:
        diccionario[nombre][2]+=round((diccionario[nombre][1]/contador)*100,1)
    
    return diccionario

def interfaz_grafica_inicial():
    ventana = Tk()
    ventana.title("Juego del Memotest")
    ventana.geometry("500x270")
    ventana.resizable(0, 0)
    ventana.config(bg = "black")

    miframe = Frame()
    miframe.pack()

    miframe.config(bg = "lightblue")
    miframe.config(width = "450", height = "270")
    miframe.config(bd=10)
    miframe.config(relief = "sunken")
    
    miimagen = PhotoImage(file = "cerebro3.gif")
    cuadro_imagen = Label(miframe, image = miimagen).place(x=4, y=50)

    etiqueta_bievenidos = Label(miframe, text = "Bienvenidos al juego del memotest", font = ("Algerian", 17)).place(x=4, y=10)

    def ingreso_usuarios():
        ventana.withdraw()
        ventana_ingreso = Toplevel()
        ventana_ingreso.title('Ingreso de usuarios')
        ventana_ingreso.config(width = "410", height = "400") #originalmente el height era 270 (410 X 500)
        ventana_ingreso.config(bg = "light blue")
        ventana_ingreso.resizable(0, 0)
        
        etiqueta_ingreso = Label(ventana_ingreso, text = "Ingreso y validación de usuarios", font = ("Algerian", 17)).place(x = 4, y = 10)
        
        etiqueta_usuarios_validados = Label(ventana_ingreso, text = "Usuarios validados", font = ("Algerian", 15)).place(x = 4, y = 258)
        
        barra_desplazamiento = Scrollbar(ventana_ingreso)
        
        lista_usuarios_validados = Listbox(ventana_ingreso, bg = "light grey", width = 62, height = 6, yscrollcommand = barra_desplazamiento.set)
        lista_usuarios_validados.place(x = 4, y = 295)
        
        barra_desplazamiento.config(command = lista_usuarios_validados.yview)
        barra_desplazamiento.place(x = 386, y = 320)
        
        jugadores = []
        
        def validar_usuario():
            
            max_jugadores = 0
            for filas in open('jugadores_temporal.csv'):
                max_jugadores += 1
                
            archivo_configuracion = open("configuracion.csv","r")
            linea_configuracion = archivo_configuracion.read()
            maxima_cantidad_jugadores = int(linea_configuracion.split("\n", 2)[1].split(";", 1)[1])
            archivo_configuracion.close()
                
            def buscar_nombre(nombre, contrasenia):

                with open("usuarios.csv", "r") as usuario1:
                    linea = usuario1.read()
                    ubicacion_linea = 0
                    contador_splitn = 1
                    contador_splitcoma = 2
                    lineanombre, lineacontrasenia, lineacomida = linea.split('\n', contador_splitn)[ubicacion_linea].split(";", contador_splitcoma)
                        
                    encontrado = False
                    contador_linea = 1
                    
                    try:
                        if nombre == "" or contrasenia == "":
                            messagebox.showerror("Atención", "No puede dejar campos vacios si quiere validar usuarios. Vuelva a intentarlo", parent = ventana_ingreso)
                            cuadro_usuario.delete(0, END)
                            cuadro_contrasenia.delete(0, END)
                            cuadro_usuario.focus_set()
                        elif nombre in jugadores:
                            messagebox.showerror("Atención", "El usuario que intenta validar ya se encuentra registrado. Pruebe con otro usuario", parent = ventana_ingreso)
                            cuadro_usuario.delete(0, END)
                            cuadro_contrasenia.delete(0, END)
                            cuadro_usuario.focus_set()
                        else:
                            while not encontrado and lineanombre:
                                if nombre in lineanombre and contrasenia in lineacontrasenia:
                                    with open("jugadores_temporal.csv", "a", newline = "") as usuarios_archivo:
                                        usuarios_actualizado = csv.writer(usuarios_archivo, dialect = 'excel', delimiter = ";")
                                        usuarios_actualizado.writerows([[nombre]])
                                    jugadores.append(nombre)
                                    messagebox.showinfo("Atención", "El usuario ha sido correctamente registrado", parent = ventana_ingreso)
                                    encontrado = True
                                else:
                                    contador_linea += 1
                                    ubicacion_linea += 1
                                    contador_splitn += 1
                                    contador_splitcoma = 2
                                    lineanombre, lineacontrasenia, lineacomida = linea.split('\n', contador_splitn)[ubicacion_linea].split(";", contador_splitcoma)
                    except:
                        messagebox.showerror("Atención", "No existe usuario registrado con los datos provistos. Vuelva a intentarlo", parent = ventana_ingreso)
                        cuadro_usuario.delete(0, END)
                        cuadro_contrasenia.delete(0, END)
                        cuadro_usuario.focus_set()
                
                return encontrado
            
            encontrado = buscar_nombre(usuario.get(),contrasenia.get())
            
            if max_jugadores + 1 <= maxima_cantidad_jugadores:
                if encontrado:
                    lista_usuarios_validados.insert(END, usuario.get())
                    cuadro_usuario.delete(0, END)
                    cuadro_contrasenia.delete(0, END)
                    cuadro_usuario.focus_set()
                else:
                    cuadro_usuario.delete(0, END)
                    cuadro_contrasenia.delete(0, END)
                    cuadro_usuario.focus_set()
            else:
                lista_usuarios_validados.insert(END, usuario.get())
                messagebox.showwarning("Atención", "Se ha alcanzado la máxima cantidad de jugadores permitida. Comenzará el juego", parent = ventana_ingreso)
                ventana_ingreso.destroy()
                ventana.destroy()
                main()
                
        def menu_principal_aviso():
            mensaje = messagebox.askokcancel("Atención", "Volver al menú principal eliminará las validaciones hechas hasta el momento. ¿Desea continuar?", parent = ventana_ingreso)
            if mensaje:
                ventana_ingreso.destroy()
                ventana.deiconify()
                archivo = "jugadores_temporal.csv"
                archivo_resetear = open(archivo, "w+")
                archivo_resetear.close()
        
        def recuperar_contrasenia():
            ventana_recuperar_contrasenia = Toplevel()
            ventana_recuperar_contrasenia.title('Recuperar contraseña')
            ventana_recuperar_contrasenia.config(width = "490", height = "135")
            ventana_recuperar_contrasenia.config(bg = "light blue")
            ventana_recuperar_contrasenia.resizable(0, 0)
            ventana_recuperar_contrasenia.grab_set()
            ventana_recuperar_contrasenia.focus_set()
            
            recuperarusuario = StringVar()
            recuperarcomida = StringVar()
            
            etiqueta_recuperar_contrasenia = Label(ventana_recuperar_contrasenia, text = "Su contraseña es:", width = 25, font = (15), anchor = "w").place(x = 8, y = 102)
            etiqueta_recuperar_contrasenia2 = Label(ventana_recuperar_contrasenia, text = "", width = 25, font = (15), anchor = "w")
            etiqueta_recuperar_contrasenia2.place(x = 250, y = 102)
            
            def volver():
                ventana_recuperar_contrasenia.destroy()
            
            def obtener_contrasenia():
                recuperar_usuario1 = recuperarusuario.get()
                recuperar_comida1 = recuperarcomida.get()
                
                filas_usuarios_csv = 0
                for filas in open('usuarios.csv'):
                    filas_usuarios_csv +=1
                
                with open("usuarios.csv", "r") as usuario1:
                    linea = usuario1.read()
                    ubicacion_linea = 0
                    contador_splitn = 1
                    contador_splitcoma = 2
                    lineanombre, lineacontrasenia, lineacomida = linea.split('\n', contador_splitn)[ubicacion_linea].split(";", contador_splitcoma)
                        
                    encontrado = False
                    contador_linea = 1
                    
                    try:
                        if recuperar_usuario1 == "" or recuperar_comida1 == "":
                            messagebox.showerror("Atención", "No puede dejar campos vacios si quiere recuperar la contraseña. Vuelva a intentarlo", parent = ventana_recuperar_contrasenia)
                            etiqueta_recuperar_contrasenia2.config(text = "")
                            cuadro_usuario_reccontra.delete(0, END)
                            cuadro_pregunta_seguridad.delete(0, END)
                            cuadro_usuario_reccontra.focus_set()
                        else:
                            while not encontrado and lineanombre:
                                if recuperar_usuario1 in lineanombre and recuperar_comida1 in lineacomida:
                                    etiqueta_recuperar_contrasenia2.config(text = lineacontrasenia)
                                    encontrado = True
                                else:
                                    contador_linea += 1
                                    ubicacion_linea += 1
                                    contador_splitn += 1
                                    contador_splitcoma = 2
                                    lineanombre, lineacontrasenia, lineacomida = linea.split('\n', contador_splitn)[ubicacion_linea].split(";", contador_splitcoma)
                    except:
                        messagebox.showerror("Atención", "No existe usuario registrado con los datos provistos. Vuelva a intentarlo", parent = ventana_recuperar_contrasenia)
                        etiqueta_recuperar_contrasenia2.config(text = "")
                        cuadro_usuario_reccontra.delete(0, END)
                        cuadro_pregunta_seguridad.delete(0, END)
                        cuadro_usuario_reccontra.focus_set()

                return    
            
            etiqueta_usuario_reccontra = Label(ventana_recuperar_contrasenia, text = "Nombre de usuario:", width = 25, font = (15), anchor = "w").place(x = 8, y = 4)
            cuadro_usuario_reccontra = Entry(ventana_recuperar_contrasenia, textvariable = recuperarusuario, width = 25, font = (15))
            cuadro_usuario_reccontra.place(x = 250, y = 4)
            
            etiqueta_pregunta_seguridad = Label(ventana_recuperar_contrasenia, text = "Comida favorita:", width = 25, font = (15), anchor = "w").place(x = 8, y = 35)
            cuadro_pregunta_seguridad = Entry(ventana_recuperar_contrasenia, textvariable = recuperarcomida, width = 25, font = (15))
            cuadro_pregunta_seguridad.place(x = 250, y = 35)
            
            boton_obtener_contraseña = Button(ventana_recuperar_contrasenia, text = "Obtener contraseña", width = 25, font = (15),  command = obtener_contrasenia).place(x = 8, y = 65)
            boton_menup = Button(ventana_recuperar_contrasenia, text = "Volver", width = 25, font = (15),  command = volver).place(x = 250, y = 65)
            
        def comenzar_juego():
            ventana_ingreso.destroy()
            ventana.destroy()
            main()
    
        etiqueta_usuario = Label(ventana_ingreso, text="Nombre de usuario o jugador", width = 23, font = (15), anchor = "w").place(x=4, y=50)
        etiqueta_contrasenia = Label(ventana_ingreso, text="Contraseña", width = 23, font = (15), anchor = "w").place(x=4, y=90)
        
        usuario = StringVar()
        contrasenia = StringVar()
        
        cuadro_usuario = Entry(ventana_ingreso, textvariable=usuario, font = (15))
        cuadro_usuario.place(x=222, y=50)
        cuadro_contrasenia = Entry(ventana_ingreso, textvariable=contrasenia, font = (15))
        cuadro_contrasenia.place(x=222, y=90)
        cuadro_contrasenia.config(show = "*")
        
        boton_validar_usuario = Button(ventana_ingreso, text = "Validar usuario", width = 20, font = (15),  command = validar_usuario).place(x=112, y=125)
        boton_menu_principal = Button(ventana_ingreso, text = "Volver al menu principal", width = 20, font = (15),  command = menu_principal_aviso).place(x=211, y=170)
        boton_comenzar_juego = Button(ventana_ingreso, text = "Comenzar juego", width = 20, font = (15),  command = comenzar_juego).place(x=112, y=215)
        boton_recuperar_contrasenia = Button(ventana_ingreso, text = "Recuperar contraseña", width = 20, font = (15),  command = recuperar_contrasenia).place(x=11, y=170)
            
    def usuarios_nuevos():
        ventana.withdraw()
        ventana_usuario_nuevo = Toplevel()
        ventana_usuario_nuevo.title('Ingreso de usuarios')
        ventana_usuario_nuevo.config(width = "442", height = "560")
        ventana_usuario_nuevo.config(bg = "light blue")
        ventana_usuario_nuevo.resizable(0, 0)
        
        etiqueta_registro = Label(ventana_usuario_nuevo, text = "Registro de nuevos usuarios", font = ("Algerian", 17)).place(x=45, y=10)

        etiqueta_usuario_nuevo = Label(ventana_usuario_nuevo, text="Nombre de usuario o jugador", width = 23, font = (15), anchor = "w").place(x=4, y=50)
        etiqueta_contrasenia_nueva = Label(ventana_usuario_nuevo, text="Contraseña", width = 23, font = (15), anchor = "w").place(x=4, y=90)
        etiqueta_confirmacion_contrasenia_nueva = Label(ventana_usuario_nuevo, text="Confirmar la contraseña", width = 23, font = (15), anchor = "w").place(x=4, y=130)
        etiqueta_pregunta_seguridad = Label(ventana_usuario_nuevo, text="Pregunta de seguridad", width = 23, font =(15), anchor ="w").place(x=4, y=170)
        etiqueta_comida_favorita = Label(ventana_usuario_nuevo, text="¿Cuál es tu comida favorita?", width = 23, font =(15), anchor ="w").place(x=4, y=196)
        
        def registrar_usuario():
            nombre = usuario_nuevo.get()
            contrasenia = contrasenia_nueva.get()
            contrasenia2 = contrasenia_nueva_confirmar.get()
            preguntaseguridad = pregunta_seguridad.get()
            validaN = validar_nombre(nombre)
            validaC = validar_contrasenia(contrasenia)
            validaI = contrasenia_igual(contrasenia, contrasenia2)
            
            def leer(archivo):
                linea = archivo.readline()
                if linea:
                    linea_csv = linea.rstrip("\n").split(";")
                else:
                    linea_csv = "", "", ""
                return linea_csv
            
            filas_usuarios_csv = 0
            for filas in open('usuarios.csv'):
                filas_usuarios_csv += 1
            
            usuario = open("usuarios.csv", "r")
            lineanombre, lineacontrasenia, lineacomida = leer(usuario)
            encontrado = False
            linea = 1
            while not encontrado and linea <= filas_usuarios_csv:
                linea += 1
                if nombre in lineanombre:
                    encontrado = True
                    
            if nombre == "":
                messagebox.showerror("Atención","Debe completar su nombre de usuario para registrarse")
            elif encontrado:
                messagebox.showerror("Atención", "El nombre de usuario ingresado ya se encuentra registrado. Vuelva a intentarlo", parent = ventana_usuario_nuevo)
            else:
                if not validaN:
                    if not validaC:
                        if len(pregunta_seguridad.get()) > 30 or len(pregunta_seguridad.get()) == 0:
                            messagebox.showerror("Atención","El usuario, la contraseña y la pregunta de seguridad ingresadas no cumplen con los requisitos detallados. Vuelva a intentarlo", parent = ventana_usuario_nuevo)
                        else:
                            messagebox.showerror("Atención","El usuario y la contraseña ingresadas no cumplen con los requisitos detallados. Vuelva a intentarlo", parent = ventana_usuario_nuevo)
                    else:
                        if len(pregunta_seguridad.get()) > 30 or len(pregunta_seguridad.get()) == 0:
                            messagebox.showerror("Atención","El usuario y la pregunta de seguridad ingresadas no cumplen con los requisitos detallados. Vuelva a intentarlo", parent = ventana_usuario_nuevo)
                        else:
                            messagebox.showerror("Atención","El usuario ingresado no cumple con los requisitos detallados. Vuelva a intentarlo", parent = ventana_usuario_nuevo)
                else:
                    if not validaC:
                        if len(pregunta_seguridad.get()) > 30 or len(pregunta_seguridad.get()) == 0:   
                            messagebox.showerror("Atención","La contraseña y la pregunta de seguridad ingresadas no cumplen con los requisitos detallados. Vuelva a intentarlo", parent = ventana_usuario_nuevo)
                        else:
                            messagebox.showerror("Atención","La contraseña ingresada no cumple con los requisitos detallados. Vuelva a intentarlo", parent = ventana_usuario_nuevo)
                    elif not validaI:
                        if len(pregunta_seguridad.get()) > 30 or len(pregunta_seguridad.get()) == 0:
                            messagebox.showerror("Atención","Las contraseñas ingresadas no coinciden y la pregunta de seguridad no cumple con los requisitos detallado. Vuelva a intentarlo", parent = ventana_usuario_nuevo)
                        else:
                            messagebox.showerror("Atención","Las contraseñas ingresadas no coinciden. Vuelva a intentarlo", parent = ventana_usuario_nuevo)
                    else:
                        if len(pregunta_seguridad.get()) > 30 or len(pregunta_seguridad.get()) == 0:
                            messagebox.showerror("Atención","La pregunta de seguridad no cumple con los requisitos detallados. Vuelva a intentarlo", parent = ventana_usuario_nuevo)
                        else:
                            agregar_a_archivos(nombre, contrasenia,preguntaseguridad)
                            messagebox.showinfo("Atención","El usuario ha sido correctamente registrado", parent = ventana_usuario_nuevo)
                            cuadro_usuario_nuevo.delete(0, END)
                            cuadro_contrasenia_nuevo.delete(0, END)
                            cuadro_confirmar_contrasenia_nuevo.delete(0, END)
                            cuadro_pregunta_seguridad.delete(0, END)
                            cuadro_usuario_nuevo.focus_set()
   
        def menu_principal():
            ventana_usuario_nuevo.destroy()
            ventana.deiconify()
            
        usuario_nuevo = StringVar()
        contrasenia_nueva = StringVar()
        contrasenia_nueva_confirmar = StringVar()
        pregunta_seguridad = StringVar()
        
        cuadro_usuario_nuevo = Entry(ventana_usuario_nuevo, textvariable=usuario_nuevo, width = 23, font = (15))
        cuadro_usuario_nuevo.place(x=222, y=50)
        cuadro_contrasenia_nuevo = Entry(ventana_usuario_nuevo, textvariable=contrasenia_nueva, width = 23, font = (15))
        cuadro_contrasenia_nuevo.place(x=222, y=90)
        cuadro_contrasenia_nuevo.config(show = "*")
        cuadro_confirmar_contrasenia_nuevo = Entry(ventana_usuario_nuevo, textvariable=contrasenia_nueva_confirmar, width = 23, font = (15))
        cuadro_confirmar_contrasenia_nuevo.place(x=222, y=130)
        cuadro_confirmar_contrasenia_nuevo.config(show = "*")
        cuadro_pregunta_seguridad = Entry(ventana_usuario_nuevo, textvariable=pregunta_seguridad, width = 23, font = (15))
        cuadro_pregunta_seguridad.place(x=222, y=196)
        
        boton_registrar_usuario = Button(ventana_usuario_nuevo, text = "Registrar usuario", width = 23, font = (15),  command = registrar_usuario).place(x=4, y=235)
        boton_menu_principal = Button(ventana_usuario_nuevo, text = "Volver al menu principal", width = 23, font = (15),  command = menu_principal).place(x=222, y=235)

        etiqueta_atencion = Label(ventana_usuario_nuevo, text="Atención", bg = "yellow", font = (10), anchor = "w").place(x=4, y=280)
        etiqueta_usuario_atencion = Label(ventana_usuario_nuevo, text="El nombre de usuario debe tener como mínimo 4 caracteres y como máximo 15 y estar formado sólo por letras, números y el guión bajo '_'", bg = "yellow", font = (10), anchor = "w", wraplength = 435).place(x=4, y=310)
        etiqueta_contrasenia_atencion = Label(ventana_usuario_nuevo, text="La contraseña debe tener como mínimo 8 caracteres y como máximo 12. No debe contener letras acentuadas. Debe contener al menos una letra mayúscula, una letra minúscula, un número y alguno de los siguientes caracteres: '-' '_'", bg = "yellow", font = (10), anchor = "w", wraplength = 435).place(x=4, y=378)
        etiqueta_seguridad_atencion = Label(ventana_usuario_nuevo, text="La pregunta de seguridad será usada para recuperar la contra seña en caso de extraviarla. La respuesta es obligatoria. Puede escribir hasta 30 caracteres de cualquier tipo como máximo", bg = "yellow", font = (10), anchor = "w", wraplength = 435).place(x=4, y=465)
        
    def configuracion():
        ventana.withdraw()
        ventana_configuracion = Toplevel()
        ventana_configuracion.title('Configuración')
        ventana_configuracion.config(width = "522", height = "495")
        ventana_configuracion.config(bg = "light blue")
        ventana_configuracion.resizable(0, 0)
        
        etiqueta_configuracion = Label(ventana_configuracion, text = "Configuración de parámetros", font = ("Algerian", 17)).place(x=75, y=10)
        etiqueta_parametros_personalizados = Label(ventana_configuracion, text="Parámetros personalizados", width = 20, anchor = "c").place(x=222, y=50)
        etiqueta_parametros_default = Label(ventana_configuracion, text="Parámetros por default", width = 20, anchor = "c").place(x=372, y=50)

        etiqueta_cantidad_fichas = Label(ventana_configuracion, text="Cantidad de fichas", width = 23, font = (15), anchor = "w").place(x=4, y=75)
        etiqueta_maximo_jugadores = Label(ventana_configuracion, text="Máximo número de jugadores", width = 23, font = (15), anchor = "w").place(x=4, y=115)
        etiqueta_maximo_partidas = Label(ventana_configuracion, text="Máximo número de partidas", width = 23, font = (15), anchor = "w").place(x=4, y=155)
        etiqueta_reiniciar_archivo_partidas = Label(ventana_configuracion, text="Resetear archivo de partidas", width = 23, font = (15), anchor = "w").place(x=4, y=195)
        
        etiqueta_fichas_default = Label(ventana_configuracion, text="16", width = 11, font = (15), anchor = "c").place(x=392, y=75)
        etiqueta_jugadores_default = Label(ventana_configuracion, text="2", width = 11, font = (15), anchor = "c").place(x=392, y=115)
        etiqueta_partidas_default = Label(ventana_configuracion, text="5", width = 11, font = (15), anchor = "c").place(x=392, y=155)
        etiqueta_reiniciar_partidas_default = Label(ventana_configuracion, text="FALSE", width = 11, font = (15), anchor = "c").place(x=392, y=195)
        
        etiqueta_atencion = Label(ventana_configuracion, text="Atención:", bg = "yellow", font = (10)).place(x=4, y=315)
        etiqueta_atencion_fichas = Label(ventana_configuracion, text="Parámetro Cantidad de fichas sólo admite valores pares múltiplos de 4. Mín 4, Máx 52 ", bg = "yellow", font = (10), wraplength = 525).place(x=4, y=345)
        etiqueta_atencion_jugadores_partidas = Label(ventana_configuracion, text="Parámetros Máximo número de jugadores admite 2 como mínimo y Máxi mo número de partidas admite 1 como mínimo", bg = "yellow", font = (10), wraplength = 525).place(x=4, y=395)
        etiqueta_atencion_reseteo_parametros = Label(ventana_configuracion, text="Parámetro Resetear archivo de partidas en modo FALSE guardará y acu mulará las estadísticas del juego una vez finalizado el mismo", bg = "yellow", font = (10), wraplength = 525).place(x=4, y=445)
        
        cantidad_fichas = StringVar()
        maximo_jugadores = StringVar()
        maximo_partidas = StringVar()
        reiniciar_archivo_partidas = StringVar()
        
        cuadro_cantidad_fichas = Entry(ventana_configuracion, textvariable = cantidad_fichas, width = 11, font = (15), justify = "center")
        cuadro_cantidad_fichas.place(x = 242, y = 75)
        cuadro_maximo_jugadores = Entry(ventana_configuracion, textvariable = maximo_jugadores, width = 11, font = (15), justify = "center")
        cuadro_maximo_jugadores.place(x = 242, y = 115)
        cuadro_maximo_partidas = Entry(ventana_configuracion, textvariable = maximo_partidas, width = 11, font = (15), justify = "center")
        cuadro_maximo_partidas.place(x = 242, y = 155)
        cuadro_reiniciar_archivo_partidas = OptionMenu(ventana_configuracion, reiniciar_archivo_partidas, "FALSE", "TRUE")
        cuadro_reiniciar_archivo_partidas.config(width = 10, height = 1)
        cuadro_reiniciar_archivo_partidas.place(x = 242, y = 195)
        
        def leer(archivo):
            linea = archivo.readline()
            if linea:
                linea_csv = linea.rstrip("\n").split(";")
            else:
                linea_csv = "", ""
            return linea_csv
        
        def parametros_personalizados():
            archivo = open('configuracion.csv','r')
            
            cantidad_fichas, cantidad_fichas_valor = leer(archivo)
            maximo_jugadores, maximo_jugadores_valor = leer(archivo)
            maximo_partidas, maximo_partidas_valor = leer(archivo)
            reiniciar_archivo_partidas, reiniciar_archivo_partidas_valor = leer(archivo)
            
            archivo.close()
            
            return cantidad_fichas_valor, maximo_jugadores_valor, maximo_partidas_valor, reiniciar_archivo_partidas_valor
        
        cantidad_fichas_valor, maximo_jugadores_valor, maximo_partidas_valor, reiniciar_archivo_partidas_valor = parametros_personalizados()
        
        cantidad_fichas_valor = int(cantidad_fichas_valor)
        maximo_jugadores_valor = int(maximo_jugadores_valor)
        maximo_partidas_valor = int(maximo_partidas_valor)
        
        cantidad_fichas.set(cantidad_fichas_valor)
        maximo_jugadores.set(maximo_jugadores_valor)
        maximo_partidas.set(maximo_partidas_valor)
        reiniciar_archivo_partidas.set(reiniciar_archivo_partidas_valor)
        
        def resetear_parametros():
            cantidad_fichas.set(16)
            maximo_jugadores.set(2)
            maximo_partidas.set(5)
            reiniciar_archivo_partidas.set("FALSE")
            cuadro_cantidad_fichas.focus_set()
            messagebox.showinfo("Atención", "Los parámetros han sido reseteados. Recuerde guardar ántes de salir.", parent = ventana_configuracion)
            
        def guardar_cambios():
            try:
                if 4 <= int(cantidad_fichas.get()) <= 52 and int(cantidad_fichas.get()) % 4 == 0:
                    if int(maximo_jugadores.get()) >= 2 and int(maximo_partidas.get()) >= 1:
                        with open ("configuracion.csv", "w", newline = "\n") as configuracion:
                            archivo_actualizado = csv.writer(configuracion, dialect = 'excel', delimiter = ";")
                            archivo_actualizado.writerows([["CANTIDAD_FICHAS",cantidad_fichas.get()],["MAXIMO_JUGADORES",maximo_jugadores.get()],["MAXIMO_PARTIDAS",maximo_partidas.get()],["REINICIAR_ARCHIVO_PARTIDAS",reiniciar_archivo_partidas.get()]])
                            messagebox.showinfo("Atención", "Los cambios han sido guardados exitosamente. Ya puede volver al menú principal", parent = ventana_configuracion)
                    else:
                        messagebox.showerror("Atención","Ingresó parámetros incorrectos en Máximo número de jugadores y/o Máximo número de partidas. Vuelva a intentarlo", parent = ventana_configuracion) 
                else:
                    messagebox.showerror("Atención","Ingresó un parámetro inválido para Cantidad de fichas. Vuelva a intentarlo", parent = ventana_configuracion)
            except:
                messagebox.showerror("Atención","Ingresó parámetros incorrectos en 1 o varios campos. Lea la sección Atención para más información y vuélvalo a intentar", parent = ventana_configuracion)
                    
        def menu_principal():
            ventana_configuracion.destroy()
            ventana.deiconify()
        
        boton_resetear_parametros = Button(ventana_configuracion, text = "Resetear parámetros", width = 23, font = (15),  command = resetear_parametros).place(x=34, y=236)
        boton_guardar_cambios = Button(ventana_configuracion, text = "Guardar cambios", width = 23, font = (15),  command = guardar_cambios).place(x=270, y=236)
        boton_menu_principal = Button(ventana_configuracion, text = "Volver al menú principal", width = 23, font = (15),  command = menu_principal).place(x=150, y=276)

    def salir():
        ventana.destroy()
        archivo = "jugadores_temporal.csv"
        archivo_resetear = open(archivo, "w+")
        archivo_resetear.close()

    boton_ingreso_usuarios = Button(miframe, text = "Ingreso de usuarios", width = 24, font = (15),  command = ingreso_usuarios).place(x=204, y=50)
    boton_usuarios_nuevos = Button(miframe, text = "Registro de usuarios nuevos", width = 24, font = (15), command = usuarios_nuevos).place(x=204, y=103)
    boton_configuracion = Button(miframe, text = "Configuración", width = 24, font = (15), command = configuracion).place(x=204, y=156)
    boton_salir = Button(miframe, text = "Salir", width = 24, font = (15), command = salir).place(x=204, y=210)

    ventana.mainloop()
    
    return

def interfaz_grafica_final(diccionario,partida,maximo_partida):
    ventana= Tk()
    ventana.title("Resultados Finales.")
    ventana.geometry("800x600")
    ventana.resizable(0, 0)
    ventana.config(bg = "black")

    miframe = Frame()
    miframe.pack()

    miframe.config(bg = "lightblue")
    miframe.config(width = "750", height = "570")
    miframe.config(bd=10)
    miframe.config(relief = "sunken")
    posicion=1
    altura=100
    jugadores=diccionario
    for nombre,puntuaciones in jugadores.items():
        etiquetas_jugadores_partida= Label(miframe, text=f"{posicion}- {nombre}",font=(15)).place(x=60,y=altura)
        etiquetas_jugadores_partida= Label(miframe, text=f"{puntuaciones[aciertos]}",font=(15)).place(x=180,y=altura)
        etiquetas_jugadores_partida= Label(miframe, text=f"{puntuaciones[intentos]}",font=(15)).place(x=290,y=altura)
        etiquetas_jugadores_partida= Label(miframe, text=f"{puntuaciones[promedio]}",font=(15)).place(x=440,y=altura)
        posicion+=1
        altura+=40

    etiqueta_titulo_ranking = Label(miframe, text = "Tabla de puntajes", font = ("Algerian", 17)).place(x=230, y=10)
    etiqueta_nombre = Label(miframe, text="Nombres", font = (15)).place(x=60, y=60)
    etiqueta_nombre = Label(miframe, text="Aciertos", font = (15)).place(x=180, y=60)
    etiqueta_nombre = Label(miframe, text=" Total de intentos ", font = (15)).place(x=290, y=60)
    etiqueta_nombre = Label(miframe, text=" Promedio de intentos ", font = (15)).place(x=440, y=60)



    Imagen_Ganador = PhotoImage(file = "medalla_1.png")
    cuadro_imagen = Label(miframe, image = Imagen_Ganador).place(x=20, y=90)
    

    def resumen_final():
        ventana.withdraw()
        ventana_resumen = Toplevel()
        ventana_resumen.title('Resumen Partidas.')
        ventana_resumen.config(width = "600", height = "270")
        ventana_resumen.config(bg = "light blue")
        ventana_resumen.resizable(1, 1)
        

        etiqueta_resumen = Label(ventana_resumen, text = "Resumen de Partidas", font = ("Algerian", 17)).place(x=170, y=10)
        etiqueta_fecha = Label(ventana_resumen, text="Fecha", font = (15)).place(x=20, y=50)
        etiqueta_hora = Label(ventana_resumen, text="Hora", font = (15)).place(x=100, y=50)
        etiqueta_nombre = Label(ventana_resumen, text=" Nombre ", font = (15)).place(x=180, y=50)
        etiqueta_aciertos = Label(ventana_resumen, text=" Aciertos ", font = (15)).place(x=290, y=50)
        etiqueta_intentos = Label(ventana_resumen, text="Intentos", font = (15)).place(x=410, y=50)

        with open("partidas.csv","r") as partidas:
            altura=100
            for lineas in partidas:
                fecha_partida,hora_finalizacion,nombre_jugador,aciertos,intentos=lineas.rstrip("\n").split(";")
                etiqueta_fecha = Label(ventana_resumen, text=fecha_partida,bg="light blue", fg="Red", font = (15)).place(x=20, y=altura)
                etiqueta_fecha = Label(ventana_resumen, text=hora_finalizacion,bg="light blue",fg="Red", font = (15)).place(x=100, y=altura)
                etiqueta_fecha = Label(ventana_resumen, text=nombre_jugador,bg="light blue",fg="Red", font = (15)).place(x=180, y=altura)
                etiqueta_fecha = Label(ventana_resumen, text=aciertos,bg="light blue",fg="Red", font = (15)).place(x=290, y=altura)
                etiqueta_fecha = Label(ventana_resumen, text=intentos,bg="light blue",fg="Red", font = (15)).place(x=410, y=altura)
                altura+=20
                
        def salir_resumen():
            ventana_resumen.destroy()
            borrar_temporales()
            
        boton_salir_resumen=Button(ventana_resumen,text="Salir",width=10,font=(15),command=salir_resumen).place(x=480,y=10)
        
    def partida_nueva():
        ventana.destroy()
        main()
       
    if not partida >= maximo_partida:
        boton_ingreso_usuarios = Button(miframe, text = "Partida nueva", width = 24, font = (15),command=partida_nueva).place(x=60, y=500)
    boton_usuarios_nuevos = Button(miframe, text = "Terminar Juego", width = 24, font = (15),command=resumen_final).place(x=300, y=500)
    
    ventana.mainloop()
    return

def borrar_temporales():
    with open("jugadores_temporal.csv", "w") as archivo:
        pass

def agregar_resumen(diccionario_ordenado,hora_finalizacion,fecha_partida):
            
    try:
        partidas=open("partidas.csv","w")
    except FileNotFoundError:
        print("Archivo no encontrado.")
    else:
        for nombre,puntajes in diccionario_ordenado.items():
            partidas.write(str(fecha_partida))
            partidas.write(";")
            partidas.write(str(hora_finalizacion))
            partidas.write(";")
            partidas.write(nombre)
            partidas.write(";")
            partidas.write(str(+puntajes[0]))
            partidas.write(";")
            partidas.write(str(+puntajes[1]))
            partidas.write("\n")
        partidas.close()
def main():
    """
    Autor: en conjunto
    
    En esta función se inicia el juego, se llama a las demás funciones que forman el programa
    y da información sobre la partida, desde que se inicia hasta su fin.
    """
    tiempo_inicial = default_timer()
        # la matriz de jugadores proviene de la interfaz grafica de tkinter
    global partida
    archivo_configuracion = open("configuracion.csv","r")
    linea_configuracion = archivo_configuracion.read()
    cantidad_fichas_tk = int(linea_configuracion.split("\n", 2)[0].split(";", 1)[1])
    cantidad_partidas_tk = int(linea_configuracion.split("\n", 3)[2].split(";", 1)[1])
    resetear_partidas_tk = linea_configuracion.split("\n", 4)[3].split(";", 1)[1]
    archivo_configuracion.close()

    FILAS = int(cantidad_fichas_tk / 4)
    COLUMNAS = 4
    VALOR = 4
    maximo_partida = cantidad_partidas_tk
    RESETEAR_PARTIDAS = resetear_partidas_tk
    
    matriz_jugadores = open("jugadores_temporal.csv").read().splitlines()
    diccionario_jugadores=crear_diccionario(matriz_jugadores)
    random.shuffle(matriz_jugadores)
    turno_jugador = matriz_jugadores
    
    print("Comenzará jugando:", turno_jugador[JugadorTurno])
    
    matriz_posiciones_apiladas, matriz_letras_apiladas = matriz_juego(FILAS, COLUMNAS, VALOR)
    mostrar_fichas_posiciones(matriz_posiciones_apiladas, FILAS, COLUMNAS)
    letras_descubiertas = 0  # contador de letras descubiertas
    contador_intentos = 0
    
    
    while letras_descubiertas < int(FILAS * COLUMNAS / 2):
        contador_posicion = 1
        posicion1 = pedir_validar_posiciones(matriz_posiciones_apiladas, contador_posicion, FILAS, COLUMNAS, VALOR) - 1
        ficha1, matriz_posiciones_apiladas, matriz_letras_apiladas = buscar_reemplazar_posiciones(
            matriz_posiciones_apiladas, matriz_letras_apiladas, posicion1, VALOR)
        mostrar_fichas_posiciones(matriz_posiciones_apiladas, FILAS, COLUMNAS)

        contador_posicion = 2
        posicion2 = pedir_validar_posiciones(matriz_posiciones_apiladas, contador_posicion, FILAS, COLUMNAS, VALOR) - 1
        ficha2, matriz_posiciones_apiladas, matriz_letras_apiladas = buscar_reemplazar_posiciones(
            matriz_posiciones_apiladas, matriz_letras_apiladas, posicion2, VALOR)
        mostrar_fichas_posiciones(matriz_posiciones_apiladas, FILAS, COLUMNAS)
        
        nombre = ""

        if ficha1 != ficha2:
            matriz_posiciones_apiladas, matriz_letras_apiladas = resetear_matriz_posiciones(matriz_posiciones_apiladas,
                                                                                            matriz_letras_apiladas,
                                                                                            posicion1, posicion2, FILAS, COLUMNAS, VALOR)

            if turno_jugador == turno_jugador[JugadorTurno]:
                contador_intentos += 1
                nombre += turno_jugador[JugadorTurno]
                modificar_diccionario_intentos(nombre, diccionario_jugadores)
                print("Mala suerte", turno_jugador[0],
                    "las posiciones seleccionadas no tenian la misma letra. Le toca jugar a",
                    turno_jugador[JugadorSiguiente])
                primer_nombre = turno_jugador.pop(0)
                turno_jugador.append(primer_nombre)
            else:
                contador_intentos += 1
                nombre += turno_jugador[JugadorTurno]
                modificar_diccionario_intentos(nombre, diccionario_jugadores)
                print("Mala suerte", turno_jugador[0],
                    "las posiciones seleccionadas no tenian la misma letra. Le toca jugar a",
                    turno_jugador[JugadorSiguiente])
                primer_nombre = turno_jugador.pop(0)
                turno_jugador.append(primer_nombre)

            mostrar_fichas_posiciones(matriz_posiciones_apiladas, FILAS, COLUMNAS)
        else:
            letras_descubiertas += 1
            nombre = turno_jugador[JugadorTurno]
            contador_intentos += 1
            
            if letras_descubiertas < int(FILAS * COLUMNAS / 2):
                if turno_jugador == turno_jugador[JugadorTurno]:
                    modificar_diccionario_aciertos(nombre, diccionario_jugadores)
                    print("Muy bien", turno_jugador[JugadorTurno],
                          "encontraste un par de letras iguales. Puedes continuar jugando")

                else:
                    modificar_diccionario_aciertos(nombre,diccionario_jugadores)
                    print("Muy bien", turno_jugador[0],
                              "encontraste un par de letras iguales. Puedes continuar jugando")
            else:
                contador_intentos+=1
                nombre=turno_jugador[JugadorTurno]
                
                if turno_jugador == turno_jugador[JugadorTurno]:
                    modificar_diccionario_aciertos(nombre,diccionario_jugadores)
                    print("Muy bien", turno_jugador[JugadorTurno],
                        "encontraste un par de letras iguales. Ya no quedan más letras por encontrar")
                else:
                    nombre=turno_jugador[JugadorTurno]
                    modificar_diccionario_aciertos(nombre,diccionario_jugadores)
                    print("Muy bien", turno_jugador[JugadorTurno],
                        "encontraste un par de letras iguales. Ya no quedan más letras por encontrar")
                        
                        
    partida+=1
    tiempo_final = default_timer()
    hora_finalizacion=time.strftime("%H:%M")
    fecha_partida=time.strftime("%d-%m")
    modificar_diccionario_promedio(diccionario_jugadores, contador_intentos)
    diccionario_ordenado=ordenar_diccionario(diccionario_jugadores)
    tiempo_total(tiempo_inicial, tiempo_final)
    agregar_resumen(diccionario_ordenado,hora_finalizacion,fecha_partida)
    interfaz_grafica_final(diccionario_ordenado,partida, maximo_partida)
    
    
    
    
interfaz_grafica_inicial()
