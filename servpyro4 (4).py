
import Pyro4
#import MySQLdb
import mysql.connector
import json
from bs4 import BeautifulSoup
from requests import get
import re,string
etiquetas_imagnes = list()
#cant_palabras = list()



HOST = 'localhost'
USER = 'root'
PASSWORD = ''
DATABASE = 'salud'


@Pyro4.expose
class conexion():
    def mensaje(self):
        return 'hola'

    def conectar(self):        #Establece la conexion con la base de datos
        try:
            conexion = mysql.connector.connect(host=HOST,
                                               database=DATABASE,
                                               user=USER,
                                               password=PASSWORD)
            cursor = conexion.cursor()
            if cursor:
                return "Conexion con exito"
        except mysql.connector.Error as e:

         return e

    def run_query(self, query):                    #La funcion Run Query permite realizar llamados a la base de datos
        conexion = mysql.connector.connect(host=HOST,
                                           database=DATABASE,
                                           user=USER,
                                           password=PASSWORD)
        cursor = conexion.cursor()
        cursor.execute(query)

        if query.upper().startswith('SELECT'):
            data = cursor.fetchall()  # Traer los resultados de un select
        else:
            conexion.commit()  # Hacer efectiva la escritura de datos
            data = None

        cursor.close()  # Cerrar el cursor
        #conn.close()  # Cerrar la conexi

        return data

    def ingresar_pagina(self, nombre, enlace):

        query = "INSERT INTO web (nombre,enlace) VALUES ('%s', '%s')" % ( nombre, enlace)
        self.run_query(query)
        lista = [" Pagina ingresada Correctamente"]
        cadena = json.dumps(lista)
        return cadena

    def ingresar_empresa(self, nom_empresa,enlace_empresa):

        query = "INSERT INTO empresas (Empresa,url_empresa) VALUES ('%s','%s')" % (nom_empresa,enlace_empresa)
        self.run_query(query)
        lista = [" Empresa Creada Satisfactoriamente"]
        cadena = json.dumps(lista)
        return cadena

    def ingresar_palabra(self, palabra_clave):

        query = "INSERT INTO diccionario (key_words) VALUES ('%s')" % (palabra_clave)
        self.run_query(query)
        lista = ["Ingreso la Palabra Correctamente"]
        cadena = json.dumps(lista)
        return cadena

    def ingreso_usuario(self):
        usu = raw_input("ingrese el nombre de usuario: ")
        return usu

    def validar_usuario(self, usu):
        if (usu == "cliente"):
            return True

        elif (usu == "admin"):

             return False

    def ver_paginas(self):
        query = "SELECT  id_nweb, nombre, enlace FROM web"
        result = self.run_query(query)
        #cadena = json.dumps(result)
        return result
        #lista = json.loads(cadena)
        #for i in lista:
         #   print i

    def pedir_url(self,URL):

        #URL = 'http://www.eltiempo.com/'
        try:
           recurso = get(URL)   #Obtiene la URL ingresada y la guarda en Recurso
           if recurso.status_code == 200:

               pagina = BeautifulSoup(recurso.text, 'html.parser')
               e = self.contar_palabras(URL)
               b = self.contar_imagenes(pagina)
               a = self.contar_enlaces(pagina)   #Llamados a las funciones del servidor
               c = self.palabras_claves(URL)
               d = self.redes_sociales(URL)
               f = self.penalizar(URL)

               totales= b+a+c+d                 #suma los valores arrojados de cada funcion

               query = "INSERT INTO criterios (nombre_pagina,cant_imagenes,canti_enlaces,pala_clave,Redes_Sociales,total) VALUES ( '%s','%s','%s','%s','%s','%s')" % (URL,b, a,c,d,totales)
               self.run_query(query)
               return "La cantidad de Palabras de su URL son: "+str(e) + "\n Imagenes "+str(b)+ "\n Enlaces " +str(a) + " \n Las palabras que coinciden con el contenido de la pagina son: " +str(c) + " \n La cantidad de Redes Soiales son:"+str(d) + "\n La cantidad de Palabras no debidas de su pagina son:" +str(f)

        except:


            print "El recurso solicitado no existe"

    def borrar_pagina(self, id):
        query = "DELETE FROM web WHERE id_nweb = '%s' " % (id)
        self.run_query(query)
        lista = [" Eliminada Correctamente"]
        cadena = json.dumps(lista)
        return cadena


    def contar_imagenes(self,pagina):
        enlaces = pagina.find_all('img')
        for enlace in enlaces:
            etiquetas = enlace.get('alt')
            if etiquetas != None and etiquetas != '':
                etiquetas_imagnes.append(etiquetas.upper())

        cantidad = len(etiquetas_imagnes)
        return cantidad

    def contar_enlaces(self, pagina):
        enlaces = pagina.find_all('a')
        i = 0
        for enlace in enlaces:
            i += 1
        #print "total", i

        return i



    def palabras_claves(self,URL):
        query = "SELECT key_words FROM diccionario" #llama al campo de la tabla que contiene las palabras claves
        result = self.run_query(query)              #el resultado de la consulta queda guardado en result
        cadena = json.dumps(result)                  #Se convierte encadena para facilitar el manejo
        recurso=get(URL)                             #Trae la pagina web ingresada
        palabra=BeautifulSoup(recurso.text,'html.parser').get_text()      # Beautiful soup extrae todo el codigo html de la pagina ingresada, queda en la variable palabra
        parrafo=re.sub('[%s]' % re.escape(string.punctuation),' ',palabra).split()  #saca las palabras solitas in signos ni etiquetas
        contar=0
        for a in sorted(set(parrafo)):   # ordena los elementos de la lista y comienza el ciclo a pasar por toda la lista
            if (a.isalpha() == True):    # si la cadena que es alfanumerica entra al siguiente ciclo.
                for e in range(len(cadena)): #este ciclo recorre las palabras de abstraidas de la base de datos tantas veces como la longitud de dicha cadena
                    #print cadena[e]
                    if(a == cadena[e]): #quitelo #si  se encuentran dos palabras iguales el contador se activa y va aumentando
                        contar +=1
        #query = "INSERT INTO criterios (pala_clave) VALUES ( '%s')" % (contar)
        #self.run_query(query)

        return contar

    def redes_sociales(self, URL):
            query = "SELECT red_social FROM redes"
            result = self.run_query(query)
            cadena = json.dumps(result)
            recurso = get(URL)
            palabra = BeautifulSoup(recurso.text, 'html.parser').get_text()
            parrafo = re.sub('[%s]' % re.escape(string.punctuation), ' ',
                             palabra).split()  # saca las palabras solitas in signos ni etiquetas
            contador = 0
            for a in sorted(set(parrafo)):  # ordena los elementos de la lista
                if (a.isalpha() == True):
                    for e in range(len(cadena)):
                        # print cadena[e]
                        if (a == cadena[e]):  # quitelo
                            contador += 1


            return contador

    def contar_palabras(self, URL):
                recurso = get(URL)
                palabra = BeautifulSoup(recurso.text, 'html.parser').get_text()
                parrafo = re.sub('[%s]' % re.escape(string.punctuation), ' ',
                                 palabra).split()  # saca las palabras solitas in signos ni etiquetas
                contador2 = 0
                for a in sorted(set(parrafo)):  # ordena los elementos de la lista y empieza el recorrido por ellas
                    if (a.isalpha() == True): # Si la cadena es alfabetica el contador comienza a a umentar
                        #for e in range(len(cadena)):
                            # print cadena[e]
                           # if (a == cadena[e]):  # quitelo
                                contador2 += 1
                return contador2

    def penalizar(self, URL):
                    query = "SELECT palabra FROM penalizar"
                    result = self.run_query(query)
                    cadena = json.dumps(result)
                    recurso = get(URL)
                    palabra = BeautifulSoup(recurso.text, 'html.parser').get_text()
                    parrafo = re.sub('[%s]' % re.escape(string.punctuation), ' ',
                                     palabra).split()  # saca las palabras solitas in signos ni etiquetas
                    contador4 = 0
                    for a in sorted(set(parrafo)):  # ordena los elementos de la lista
                        if (a.isalpha() == True):
                            for e in range(len(cadena)):
                                print a
                                if (a == cadena[e]):
                                    contador4 += 1
                    query = "INSERT INTO paginas_penalizadas (pagina) VALUES ( '%s')" % (URL)
                    self.run_query(query)
                    return contador4

    def ver_penalizadas(self):
                        query = "SELECT  id_pagina, pagina FROM paginas_penalizadas"
                        result = self.run_query(query)
                        #cadena = json.dumps(result)
                        return result

    def ver_ranking(self):
                            query = "SELECT  id, nombre_pagina,total  FROM criterios"
                            result = self.run_query(query)
                            #cadena = json.dumps(result)
                            return result

   # if palabra.upper() in etiquetas_imagnes:
    #        print "palabra encontrada"
    #else:
     #       print "palabra no encontrada"




            # print etiquetas
            # i in tiquetas_imagnes:
            # contador+=1

            # return contador

        #print 'la cantidad de etiquetas son', cantidad



    #def contar_palabras(self, pagina):
         #   palabras = pagina.find_all('.')
          #  if palabras.upper() in cant_palabras:
           #     print 'palabra encontrada'
            #else:
             #   print 'palabra no encontrada'






def main():

    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(conexion)
    ns.register('fausto.com', uri)
    daemon.requestLoop()


if __name__ == '__main__':
    main()


