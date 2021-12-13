def leer_usuarios(usuario):
    leer_linea=usuario.readline()
    if leer_linea:
        linea=leer_linea.rstrip("\n").split(";")
    else:
        linea="",""
    return linea

def buscar_nombre(nombre,contrasenia):
    jugadores=[]
    encontrado=False
    try:
        usuario=open("usuario.csv","r")
    except FileNotFoundError:
        print("El archivo no existe")
    else:
        LineaNombre,LineaContrasenia=leer_usuarios(usuario)
        while not encontrado and LineaNombre:
            if nombre in LineaNombre and contrasenia in LineaContrasenia:
                jugadores.append(nombre)
                encontrado=True
            else:
                LineaNombre,LineaContrasenia=leer_usuarios(usuario)
    usuario.close()
    return jugadores
