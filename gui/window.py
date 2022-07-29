# from the tkinter library
from tkinter import *
from tkinter import filedialog, messagebox

from numpy import insert


class Window():

    def __init__(self, parser, repository):
        self.parser = parser
        self.repository = repository
        self.data = {}
        self.window = Tk()
        self.window_config()
        self.create_labels()
        self.create_buttons()
        self.create_menus()
        # Let the window wait for any events
        self.window.mainloop()

    def create_buttons(self):
        self.button_select_file = Button(self.window,text = "Seleccionar fichero...", font=("Arial", 12), command = self.select_file)
        self.button_select_file.pack(side=TOP, fill=BOTH, padx=100, pady=10)
        self.button_add_to_bd = Button(self.window,text = "Añadir a base de datos", font=("Arial", 12), command = self.insert_data)
        self.button_add_to_bd.pack(side=TOP, fill=BOTH, padx=100, pady=10)

    def create_menus(self):
        self.menu = Menu()
        # Crear el primer menú.
        self.menu_archivo = Menu(self.menu, tearoff=False)
        self.menu_ayuda = Menu(self.menu, tearoff=False)
        # Agregarlo a la barra.
        self.menu.add_cascade(menu=self.menu_archivo, label="Archivo")
        self.menu_archivo.add_command(
            label="Salir",
            accelerator="Ctrl+Q",
            command=exit
        )
        self.menu.add_cascade(menu=self.menu_ayuda, label="Ayuda")
        self.menu_ayuda.add_command(
            label="Acerca de...",
            command=self.show_info
        )
        self.window.config(background = "white", menu=self.menu)
    
    def create_labels(self):
        # Create a File Explorer label
        self.label_file_explorer = Label(self.window,text = "Ningún fichero seleccionado.", font=("Arial", 12))
        self.label_file_explorer.pack(side=TOP, fill=BOTH, padx=20, pady=40)


    def show_info():
        messagebox.showinfo("Acerca de", "Aplicación que procesa ficheros xml de p48 de cierre de ESIOS y los almacena en una base de datos local\n\nAutor: Diego González Suárez - Universidad de Oviedo. \nContacto: uo276406@uniovi.es - diegogs1451@outlook.es")


    def window_config(self):
        # Set window title
        self.window.title('P48Manager')
        #No redimensionar ventana
        self.window.resizable(width=0, height=0)
        # Set window size
        self.window.geometry("800x300")
    
    # file explorer window
    def select_file(self):
        self.filename = filedialog.askopenfilename(initialdir = "C:/ESIOS/p48cierre",title = "Seleccione un fichero",filetypes = (("XML files","*.xml*"),("all files","*.*")))
        # Change label contents
        self.label_file_explorer.configure(text="Fichero seleccionado: " + self.filename)
        self.data = self.parser.parse(self.filename)


    def insert_data(self):
        res = self.repository.insert(self.data)
        if "Error" in res:
            messagebox.showerror("Operación inserción", res)
        else:
            messagebox.showinfo("Operación inserción", res)
