import pymongo
from tkinter.messagebox import showinfo
from tkinter import*
from tkinter import ttk
from tkinter import messagebox 
from PIL import ImageTk, Image
import os
from bson.objectid import ObjectId
from turtle import bgcolor
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox as MessageBox
from turtle import bgcolor

MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://" + MONGO_HOST + ":" + MONGO_PUERTO + "/"

MONGO_BASEDATOS="ClentamientoGlobal"
MONGO_COLECCION="GasesToxicos"
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos=cliente[MONGO_BASEDATOS]
coleccion=baseDatos[MONGO_COLECCION]
ID_ALUMNO=""
def mostrarDatos(CO = ""):
    objetoBuscar={}
    if len(CO)!=0:
        objetoBuscar["CO"]=CO
    try:
        registros=tabla.get_children()
        for registro in registros:
            tabla.delete(registro)
        for documento in coleccion.find(objetoBuscar):
            tabla.insert('',0,text=documento["_id"],values=documento["CO"])
        cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo exedido "+errorTiempo)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a mongodb "+errorConexion)
def crearRegistro():
    if len(nombre.get())!=0 and len(calificacion.get())!=0 and len(sexo.get())!=0 :
        try:
            documento={"CO":nombre.get(),"NOX":calificacion.get(),"CO2":sexo.get()}
            coleccion.insert(documento)
            nombre.delete(0,END)
            sexo.delete(0,END)
            calificacion.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrarDatos()
def dobleClickTabla(event):
    global ID_ALUMNO
    ID_ALUMNO=str(tabla.item(tabla.selection())["text"])
    #print(ID_ALUMNO)
    documento=coleccion.find({"_id":ObjectId(ID_ALUMNO)})[0]
    #print(documento)
    nombre.delete(0,END)
    nombre.insert(0,documento["CO"])
    sexo.delete(0,END)
    sexo.insert(0,documento["NOX"])
    calificacion.delete(0,END)
    calificacion.insert(0,documento["CO2"])
    crear["state"]="disabled"
    editar["state"]="normal"
    borrar["state"]="normal"
def editarRegistro():
    global ID_ALUMNO
    if len(nombre.get())!=0 and len(sexo.get())!=0 and len(calificacion.get())!=0 :
        try:
            idBuscar={"_id":ObjectId(ID_ALUMNO)}
            nuevosValores={"CO":nombre.get(),"NOX":sexo.get(),"CO2":calificacion.get()}
            coleccion.update(idBuscar,nuevosValores)
            nombre.delete(0,END)
            sexo.delete(0,END)
            calificacion.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror("Los campos no pueden estar vacios")
    mostrarDatos()
    crear["state"]="normal"
    editar["state"]="disabled"
    borrar["state"]="disabled"
def borrarRegistro():
    global ID_ALUMNO
    try:
        idBuscar={"_id":ObjectId(ID_ALUMNO)}
        coleccion.delete_one(idBuscar)
        nombre.delete(0,END)
        sexo.delete(0,END)
        calificacion.delete(0,END)
    except pymongo.errors.ConnectionFailure as error:
        print(error)
    crear["state"]="normal"
    editar["state"]="disabled"
    borrar["state"]="disabled"
    mostrarDatos()
def buscarRegistro():
    mostrarDatos(buscarNombre.get())

def mapa():
    entidad = coleccion.find()
    listaEntidades = []
    listaTotales = []

    for r in entidad:
        listaEntidades.append(r["CO"])
        listaTotales.append(r["NOX"])
    
    array1 = np.array(listaEntidades)
    array2 = np.array(listaTotales)
    
    fig, ax = plt.subplots()
    ax.set_ylabel('Gases Toxicos')
    ax.set_title('Gases')
    plt.plot(array1, array2)
    plt.show()
    

def diagrama():
    entidad = coleccion.find()
    listaEntidades = []
    listaTotales = []

    for r in entidad:
        listaEntidades.append(r["CO"])
        listaTotales.append(r["NOX"])
        
    array1 = np.array(listaEntidades)
    array2 = np.array(listaTotales)
    
    fig1, ax1 = plt.subplots()
    ax1.pie(array2, labels=array1, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('Monoxido de carbono')
    plt.title("Oxido de Nitrogeno")
    plt.legend()
    plt.show()

def grafica():
    
    entidad = coleccion.find()
    listaEntidades = []
    listaTotales = []

    for r in entidad:
        listaEntidades.append(r["CO"])
        listaTotales.append(r["NOX"])
        
    array1 = np.array(listaEntidades)
    array2 = np.array(listaTotales)

    fig, ax = plt.subplots()
    ax.set_ylabel('Monoxido de Carbono')
    ax.set_title('Oxido de Nitrigeno')
    plt.bar(array1, array2)
    plt.show()


    
#Crear Vnetana
ventana=Tk()
ventana.title("Calentamiento Global")
ventana.geometry('1400x750')
ventana.configure(bg='#FCFCF4')
img = ImageTk.PhotoImage(Image.open("Contaminacion.jpg"))
#Displaying it
imglabel = Label(ventana, image=img).grid(row=0, column=2) 
img1 = ImageTk.PhotoImage(Image.open("2.jpg"))
#Displaying it
imglabel = Label(ventana, image=img1).grid(row=0, column=0) 
tabla=ttk.Treeview(ventana,columns=2)
tabla.grid(row=0,column=2,columnspan=2)
tabla.heading("#0",text="NUMERO ID")
tabla.heading("#1",text="Monoxido de Carbono ")
tabla.bind("<Double-Button-1>",dobleClickTabla)
#Nombre
Label(ventana,text="CO").grid(row=1,column=0,sticky=W+E)
nombre=Entry(ventana)
nombre.grid(row=1,column=1,sticky=W+E)
nombre.focus()
#Sexo
Label(ventana,text="NOX").grid(row=2,column=0,sticky=W+E)
sexo=Entry(ventana)
sexo.grid(row=2,column=1,sticky=W+E)
#Calificacion
Label(ventana,text="CO2").grid(row=3,column=0,sticky=W+E)
calificacion=Entry(ventana)
calificacion.grid(row=3,column=1,sticky=W+E)
#Boton crear
crear=Button(ventana,text="Crear Registro",command=crearRegistro,bg="green",fg="white")
crear.grid(row=4,columnspan=2,sticky=W+E)
#Boton editar
editar=Button(ventana,text="Editar Registro",command=editarRegistro,bg="yellow")
editar.grid(row=5,columnspan=2,sticky=W+E)
editar["state"]="disabled"
#Boton borrar
borrar=Button(ventana,text="Borrar Registro",command=borrarRegistro,bg="red",fg="white")
borrar.grid(row=6,columnspan=2,sticky=W+E)
borrar["state"]="disabled"
#buscar Nombre
Label(ventana,text="Buscar por Monóxido de carbono").grid(row=7,column=0,sticky=W+E)
buscarNombre=Entry(ventana)
buscarNombre.grid(row=7,column=1,sticky=W+E)
buscar=Button(ventana,text="Buscar Registro",command=buscarRegistro,bg="blue",fg="white")
buscar.grid(row=8,columnspan=2,sticky=W+E)

arras = Button(text = 'GRAFICA BARRAS....', command = grafica, bg = "#FFFC33").grid(row = 9, column = 0, sticky = W + E)
pastel = Button(text = 'GRAFICA CIRCULO...', command = diagrama, bg = "#68FF33").grid(row = 10, column = 0, sticky = W + E)
area = Button(text = 'GRAFICA AREA ...', command = mapa, bg = "#33E6FF").grid(row = 11, column = 0, sticky = W + E)



mostrarDatos()
ventana.mainloop()