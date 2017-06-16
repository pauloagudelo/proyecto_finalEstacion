import Pyro4


uri = "fausto.com"
#Pyro4.sockettutil
conexion = Pyro4.Proxy('PYRONAME:'+uri)
#print conexion.conectar()
#print conexion.ingresar_pagina()



usu = raw_input("ingrese el nombre de usuario: ")

#a = conexion.ingreso_usuario()
b = conexion.validar_usuario(usu)  #asignamos a variables la funcion para que esta guarde el valor que retorna
if b == True:
    mnu = [' CLIENTE\n''1.lISTADO DE PAGINAS', '2.INGRESAR PAGINA', '3. ANALIZAR PAGINA WEB', '4. ELIMINAR PAGINA', '5. VER PAGINAS PENALIZADAS','6.RANKING PAGINAS WEB','7.SALIR']
    while b==True:
        for i in mnu:
            print i
        opcion = int(raw_input("Elija La Opcion: "))
        if opcion == 1:
            f= conexion.ver_paginas()
            for i in f:
                print i

        if opcion == 2:
            nombre = raw_input("ingrese nombre de la pagina: ")
            enlace = raw_input("ingrese enlace de la pagina: ")
            print conexion.ingresar_pagina(nombre, enlace)
            print "Su pagina ha sido Gpuardada"

        if opcion == 3:
            URL = raw_input("Ingrese direccion URL de su pagina web")

            print conexion.pedir_url(URL)


        if opcion == 4:
            print conexion.ver_paginas()
            id = int(raw_input("Ingrese el codigo de la pagina a ELiminar"))
            print conexion.borrar_pagina(id)

        if opcion == 5:

                    q= conexion.ver_penalizadas()
                    for i in q:  #utilizado para que me imprima con salto de linea y no derecho
                        print i

        if opcion == 6:
                    p= conexion.ver_ranking()
                    for i in p:
                        print i
        if opcion == 7:
            b =False

if b == False:
    mnu2 = [' ADMINISTRADOR\n''1.iNGRESAR EMPRESA', '2.INGRESAR PALABRAS CLAVE', '3. VER PAGINAS PENALIZADAS','4. RANKING PAGINAS WEB']

    for i in mnu2:
        print i
    opcion = int(raw_input("Elija La Opcion: "))
    if opcion ==1:
        nom_empresa = raw_input("ingrese nombre de la empresa: ")
        enlace_empresa=raw_input("Ingrese URL de la Empresa:")
        print conexion.ingresar_empresa(nom_empresa,enlace_empresa)
    if opcion == 2:
        palabra_clave = raw_input("Ingrese La palabra Clave : ")

        print conexion.ingresar_palabra(palabra_clave)

    if opcion == 3:
        q = conexion.ver_penalizadas()
        for i in q:
            print i

    if opcion == 4:
        p= conexion.ver_ranking()
        for i in p:
          print i
