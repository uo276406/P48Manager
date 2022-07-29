# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog, messagebox

import xml.etree.ElementTree as ET
import sqlite3
import os

global file_selected
# Array with all the combinated cicles to show
cicles_to_show = ['CTJON1','CTJON3','ACE3','ACE4','ALG3','AMBIETA','ARCOS1','ARCOS2','ARCOS3','ARRU1','ARRU2','BAHIAB','BES3','BES4','BES5','CAMGI10','CAMGI20','COL4','CTGN1','CTGN2','CTGN3','CTJON2','CTN3','CTN4','CTNU','ECT2','ECT3','ESC6','ESCCC1','ESCCC2','ESCCC3','MALA1','PALOS1','PALOS2','PALOS3','PBCN1','PBCN2','PGR5','PVENT1','PVENT2','SAGU1','SAGU2','SAGU3','SBO3','SRI4','SRI5','SROQ1','SROQ2','STC4','TAPOWER']

def create_db_file_and_table(path):
	f = open(path, 'w')
	f.close()
	con = sqlite3.connect(path)
	cur = con.cursor()
	cur.execute('CREATE TABLE P48Cierre (Ciclo TEXT, Fecha TEXT, Hora INTEGER CHECK(Hora <= 24 AND Hora >= 1), Produccion REAL,PRIMARY KEY(Ciclo,Fecha,Produccion,Hora))')
	con.commit()
	cur.close()
	con.close()


# Function for opening the
# file explorer window
def select_file():
	global file_selected
	filename = filedialog.askopenfilename(initialdir = "C:/ESIOS/p48cierre",title = "Seleccione un fichero",filetypes = (("XML files","*.xml*"),("all files","*.*")))
	# Change label contents
	label_file_explorer.configure(text="Fichero seleccionado: " + filename)
	file_selected = filename
	


def add_bd():
	# Hacemos la conexión a la base de datos, si existe el fichero
	if not os.path.exists("C:/ESIOS/p48cierre/p48cierre.db"):
		create_db_file_and_table("C:/ESIOS/p48cierre/p48cierre.db")
	try:
		data_processed = parse_xml(file_selected)
		date = os.path.basename(file_selected)
		date_list = date.split('_')
		date = date_list[1].split('.')[0]
		date = date[:4] + '-' + date[4:6] + '-' + date[6:]
		
		con = sqlite3.connect("C:/ESIOS/p48cierre/p48cierre.db")
		cur = con.cursor()
		try:
			rows = 0
			for cicle in cicles_to_show:
				try:	
					for i in range(len(data_processed[cicle])):
						# Hacemos los inserts a la base de datos
						cur.execute("INSERT INTO P48Cierre values (?,?,?,?)", (cicle, date, i+1, data_processed[cicle][i+1]))
						rows+=1	
				except KeyError:
					continue
			con.commit()
			messagebox.showinfo("Datos añadidos", "Datos añadidos a la base de datos correctamente. " + str(rows) + " Filas añadidas.")
		except sqlite3.Error:
			messagebox.showerror("Error de base de datos", "Error al insertar datos, probablemente ya añadidos")
			con.rollback()
		finally:
			cur.close()
			con.close()
		messagebox
	except FileNotFoundError:
		messagebox.showerror("Fichero no encontrado", "No se ha encontrado el fichero seleccionado")
	except ET.ParseError:
		messagebox.showerror("Error al procesar el fichero", "Problema en el procesamiento del fichero, compruebe el formato y asegurese que es de p48 de cierre.")

def parse_xml(filename):
	root = ET.parse(filename).getroot()
	res = {}
	for serie in root:
		for cicle in serie:
			if cicle.tag == '{urn:sios.ree.es:p48cierre:1:0}UPEntrada':
				if cicle.attrib['v'] in cicles_to_show:
					name_cicle = cicle.attrib['v']
					for cicle in serie:
						if cicle.tag == '{urn:sios.ree.es:p48cierre:1:0}Periodo':
							sum_cuarter = 0.
							is_cuarter = 0
							hour = 0
							data = {}
							for intervalo in cicle:
								for value in intervalo:
									if value.tag =='{urn:sios.ree.es:p48cierre:1:0}Ctd':
										sum_cuarter += float(value.attrib['v'])
										is_cuarter += 1
								if is_cuarter % 4 == 0 and is_cuarter != 0:
									hour += 1
									data[hour] = sum_cuarter
									sum_cuarter = 0
					res[name_cicle] = data
	return res
		

def show_info():
	messagebox.showinfo("Acerca de", "Aplicación que procesa ficheros xml de p48 de cierre de ESIOS y los almacena en una base de datos local\n\nAutor: Diego González Suárez - Universidad de Oviedo. \nContacto: uo276406@uniovi.es - diegogs1451@outlook.es")


# Create the root window
window = Tk()

# Set window title
window.title('P48Manager')
#No redimensionar ventana
window.resizable(width=0, height=0)
# Set window size
window.geometry("800x300")

menu = Menu()
# Crear el primer menú.
menu_archivo = Menu(menu, tearoff=False)
menu_ayuda = Menu(menu, tearoff=False)
# Agregarlo a la barra.
menu.add_cascade(menu=menu_archivo, label="Archivo")
menu_archivo.add_command(
    label="Salir",
    accelerator="Ctrl+Q",
    command=exit
)
menu.add_cascade(menu=menu_ayuda, label="Ayuda")
menu_ayuda.add_command(
    label="Acerca de...",
    command=show_info
)

# Create a File Explorer label
label_file_explorer = Label(window,text = "Ningún fichero seleccionado.", font=("Arial", 12))
label_file_explorer.pack(side=TOP, fill=BOTH, padx=20, pady=40)
button_add_to_bd = Button(window,text = "Seleccionar fichero...", font=("Arial", 12), command = select_file)
button_add_to_bd.pack(side=TOP, fill=BOTH, padx=100, pady=10)
button_add_to_bd = Button(window,text = "Añadir a base de datos", font=("Arial", 12), command = add_bd)
button_add_to_bd.pack(side=TOP, fill=BOTH, padx=100, pady=10)
# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns

window.config(background = "white", menu=menu)

# Let the window wait for any events
window.mainloop()
