from tkinter import *

def validar_nombre(nombre):
    #Valida usuario
    valido=True
    letra=0
    if 4<=len(nombre)<=15:
        while valido and not letra == len(nombre):
        
            if nombre[letra]=="_":
                valido=True
                letra+=1
            elif nombre[letra].isalnum():
                valido=True
                letra+=1
            else:
                valido=False
    else:
        valido=False
        
    return valido

def validar_contrasenia(contrasenia):
    #Valida contraseña
    letras_acentuadas=["á","é","í","o","ú"]
    letras_acentuadas_mayus=["Á","É","Í","Ó","Ú"]
    contrasenia_guion=0
    contrasenia_mayus=0
    contrasenia_minus=0
    contrasenia_numero=0
    valido=True
    letra=0
    
    if 8<=len(contrasenia)<=12:
        while valido and not letra==len(contrasenia):
            if contrasenia [letra]=="_" or contrasenia[letra]=="-":
                contrasenia_guion+=1
                letra+=1
            elif contrasenia[letra].isupper():
                contrasenia_mayus+=1
                letra+=1
            elif contrasenia[letra].islower():
                contrasenia_minus+=1
                letra+=1
            elif contrasenia[letra].isnumeric():
                contrasenia_numero+=1
                letra+=1
            elif contrasenia[letra] in letras_acentuadas or contrasenia[letra] in letras_acentuadas_mayus:
                letra+=1
            else:
                valido=False
    if contrasenia_guion==0 or contrasenia_mayus==0 or contrasenia_minus==0 or contrasenia_numero==0:
        valido=False
    
    return valido

def contrasenia_igual(contrasenia,contrasenia2):
    #Compara contraseñas
    valido=False
    if contrasenia==contrasenia2:
        valido=True
    return valido

def agregar_a_archivos(nombre,contrasenia):
    #Abre archivo usuario.csv y escribe nombre y contraseñas si son correctos
    try:
        usuario = open("usuario.csv","a")
    except FileNotFoundError:
        print("El archivo no existe")
    else:
        usuario.write(nombre)
        usuario.write(";")
        usuario.write(contrasenia)
        usuario.write("\n")
        usuario.close()

def interfaz_grafica():
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
    
    #miimagen = PhotoImage(file = "cerebro3.gif")
    #cuadro_imagen = Label(miframe, image = miimagen).place(x=4, y=50)

    etiqueta_bievenidos = Label(miframe, text = "Bienvenidos al juego del memotest", font = ("Algerian", 17)).place(x=4, y=10)

    def ingreso_usuarios():
        ventana.withdraw()
        ventana_ingreso = Toplevel()
        ventana_ingreso.title('Ingreso de usuarios')
        ventana_ingreso.config(width = "410", height = "270")
        ventana_ingreso.config(bg = "light blue")
        ventana_ingreso.resizable(0, 0)
        
        etiqueta_ingreso = Label(ventana_ingreso, text = "Ingreso y validación de usuarios", font = ("Algerian", 17)).place(x=4, y=10)
        
        jugadores = []
        
        def validar_usuario():
            
            def leer_usuarios(usuario):
                leer_linea = usuario.readline()
                if leer_linea:
                    linea = leer_linea.rstrip("\n").split(";")
                else:
                    linea = "", ""
                return linea
            
            
            def buscar_nombre(nombre, contrasenia):
                encontrado = False
                try:
                    usuario = open("usuario.csv","r")
                except FileNotFoundError:
                    print("El archivo no existe")
                else:
                    LineaNombre, LineaContrasenia = leer_usuarios(usuario)
                    while not encontrado and LineaNombre:
                        if nombre in LineaNombre and contrasenia in LineaContrasenia:
                            if not nombre in jugadores:
                                jugadores.append(nombre)
                                encontrado=True
                            #else:
                            #   pass
                        else:
                            LineaNombre, LineaContrasenia = leer_usuarios(usuario)
                usuario.close()
                #print(jugadores)
                
                return
            
            #lista_usuarios_validados.insert(END, usuario.get())
        
            buscar_nombre(usuario.get(),contrasenia.get())
        
        def siguiente_usuario():
            #esto lo único que hace es eliminar los datos cargados en los cuadros de entrada, también podría eliminarlos el
            #usuario a mano
            cuadro_usuario.delete(0, END)
            cuadro_contrasenia.delete(0, END)
            cuadro_usuario.focus_set()
            
        def menu_principal_aviso():
            ventana_aviso = Toplevel()
            ventana_aviso.title('Atención')
            ventana_aviso.config(width = "550", height = "80")
            ventana_aviso.config(bg = "light blue")
            ventana_aviso.resizable(0, 0)
            ventana_aviso.grab_set() # Mantiene el foco de la ventana hasta que se cierre
            ventana_aviso.focus_set() # Mantiene el foco cuando se abre la ventana.
            
            etiqueta_aviso = Label(ventana_aviso, text="Volver al menú principal eliminará las validaciones hechas hasta el momento", font = (12)).place(x=8, y=4)
            
            def aceptar():
                ventana_aviso.destroy()
                ventana_ingreso.destroy()
                ventana.deiconify()
                
            def volver():
                ventana_aviso.destroy()
            
            boton_aceptar = Button(ventana_aviso, text = "Aceptar", font = (15), width = 25,  command = aceptar).place(x=23, y=35)
            boton_volver = Button(ventana_aviso, text = "Volver a la carga de usuarios", width = 25, font = (15),  command = volver).place(x=290, y=35)
            
        def comenzar_juego():
            b=3
            
        def recuperar_contrasenia():
            b=4

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
        boton_siguiente_usuario = Button(ventana_ingreso, text = "Cargar siguiente usuario", width = 20, font = (15),  command = siguiente_usuario).place(x=11, y=170)
        boton_menu_principal = Button(ventana_ingreso, text = "Volver al menu principal", width = 20, font = (15),  command = menu_principal_aviso).place(x=211, y=170)
        boton_recuperar_contrasenia = Button(ventana_ingreso, text = "Recuperar contraseña", width = 20, font = (15),  command = recuperar_contrasenia).place(x=11, y=215)
        boton_comenzar_juego = Button(ventana_ingreso, text = "Comenzar juego", width = 20, font = (15),  command = comenzar_juego).place(x=211, y=215)
            
    def usuarios_nuevos():
        ventana.withdraw()
        ventana_usuario_nuevo = Toplevel()
        ventana_usuario_nuevo.title('Ingreso de usuarios')
        ventana_usuario_nuevo.config(width = "442", height = "400")
        ventana_usuario_nuevo.config(bg = "light blue")
        ventana_usuario_nuevo.resizable(0, 0)
        
        etiqueta_registro = Label(ventana_usuario_nuevo, text = "Registro de nuevos usuarios", font = ("Algerian", 17)).place(x=45, y=10)
        
        etiqueta_usuario_nuevo = Label(ventana_usuario_nuevo, text="Nombre de usuario o jugador", width = 23, font = (15), anchor = "w").place(x=4, y=50)
        etiqueta_contrasenia_nueva = Label(ventana_usuario_nuevo, text="Contraseña", width = 23, font = (15), anchor = "w").place(x=4, y=90)
        etiqueta_confirmacion_contrasenia_nueva = Label(ventana_usuario_nuevo, text="Confirmar la contraseña", width = 23, font = (15), anchor = "w").place(x=4, y=130)
        
        def registrar_usuario():
            nombre=usuario_nuevo.get()
            contrasenia=contrasenia_nueva.get()
            contrasenia2=contrasenia_nueva_confirmar.get()
            validaN=validar_nombre(nombre)
            validaC=validar_contrasenia(contrasenia)
            if validaC:
                validaI=contrasenia_igual(contrasenia,contrasenia2)
            else:
                etiqueta_error=Label(ventana_usuario_nuevo,text="Error: Contraseña incorrecta/No coinciden.", bg="Red", font=(10)).place(x=100,y=210)
            if validaI and validaN:
                agregar_a_archivos(nombre,contrasenia)
                etiqueta_error=Label(ventana_usuario_nuevo,text="USUARIO REGISTRADO.", bg="green", font=(10)).place(x=150,y=210)

                
        
        def menu_principal():
            ventana_usuario_nuevo.destroy()
            ventana.deiconify()
            
        usuario_nuevo = StringVar()
        contrasenia_nueva = StringVar()
        contrasenia_nueva_confirmar = StringVar()
        
        cuadro_usuario_nuevo = Entry(ventana_usuario_nuevo, textvariable=usuario_nuevo, width = 23, font = (15))
        cuadro_usuario_nuevo.place(x=222, y=50)
        cuadro_contrasenia_nuevo = Entry(ventana_usuario_nuevo, textvariable=contrasenia_nueva, width = 23, font = (15))
        cuadro_contrasenia_nuevo.place(x=222, y=90)
        cuadro_contrasenia_nuevo.config(show = "*")
        cuadro_confirmar_contrasenia_nuevo = Entry(ventana_usuario_nuevo, textvariable=contrasenia_nueva_confirmar, width = 23, font = (15))
        cuadro_confirmar_contrasenia_nuevo.place(x=222, y=130)
        cuadro_confirmar_contrasenia_nuevo.config(show = "*")
        
        boton_registrar_usuario = Button(ventana_usuario_nuevo, text = "Registrar usuario", width = 23, font = (15),  command = registrar_usuario).place(x=4, y=170)
        boton_menu_principal = Button(ventana_usuario_nuevo, text = "Volver al menu principal", width = 23, font = (15),  command = menu_principal).place(x=222, y=170)

        etiqueta_atencion = Label(ventana_usuario_nuevo, text="Atención", bg = "yellow", font = (10), anchor = "w").place(x=4, y=210)
        etiqueta_usuario_atencion = Label(ventana_usuario_nuevo, text="El nombre de usuario debe tener como mínimo 4 caracteres y como máximo 15 y estar formado sólo por letras, números y el guión bajo '_'", bg = "yellow", font = (10), anchor = "w", wraplength = 435).place(x=4, y=240)
        etiqueta_contrasenia_atencion = Label(ventana_usuario_nuevo, text="La contraseña debe tener como mínimo 8 caracteres y como máximo 12. No debe contener letras acentuadas. Debe contener al menos una letra mayúscula, una letra minúscula, un número y alguno de los siguientes caracteres: '-' '_'", bg = "yellow", font = (10), anchor = "w", wraplength = 435).place(x=4, y=308)
        
    def configuracion():
        #esta funcion deberia permitir setear los parámetros del juego
        b=2
        
    def salir():
        ventana.destroy()

    boton_ingreso_usuarios = Button(miframe, text = "Ingreso de usuarios", width = 24, font = (15),  command = ingreso_usuarios).place(x=204, y=50)
    boton_usuarios_nuevos = Button(miframe, text = "Registro de usuarios nuevos", width = 24, font = (15), command = usuarios_nuevos).place(x=204, y=103)
    boton_configuracion = Button(miframe, text = "Configuración", width = 24, font = (15), command = configuracion).place(x=204, y=156)
    boton_salir = Button(miframe, text = "Salir", width = 24, font = (15), command = salir).place(x=204, y=210)

    ventana.mainloop()
interfaz_grafica()
