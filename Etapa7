def validar_usuario(nombre):
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
    
    usuario = open("usuario.csv","w")
    usuario.write(nombre)
    usuario.write(";")
    usuario.write(contrasenia)
    usuario.close()

def main(nombre,contrasenia):

    validaN=validar_usuario(nombre)
    validaC=validar_contrasenia(contrasenia)
    validaI=contrasenia_igual(contrasenia,contrasenia2)
    if validaC and validaN:
        agregar_a_archivos(nombre,contrasenia)
        
