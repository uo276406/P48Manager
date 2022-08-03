# from the tkinter library
from tkinter import *
from tkinter import filedialog, messagebox
from gui.GraphicDialog import GraphicDialog


class MainWindow():

    def __init__(self, parser, repository, painter, cicles):
        self.parser = parser
        self.repository = repository
        self.painter = painter
        self.cicles = cicles
        self.data = {}
        self.window = Tk()
        self.window_config()
        self.create_labels()
        self.create_buttons()
        self.create_menus()
        # Let the window wait for any events
        self.window.mainloop()


    def create_buttons(self):
        self.button_select_file = Button(self.window,text = "Seleccionar fichero...", font=("Arial", 12), command = self.parse_file)
        self.button_select_file.pack(side=TOP, fill=BOTH, padx=100, pady=10)
        self.button_add_to_bd = Button(self.window,text = "Añadir a base de datos", font=("Arial", 12), command = self.insert_data)
        self.button_add_to_bd.pack(side=TOP, fill=BOTH, padx=100, pady=10)
        self.button_show_data = Button(self.window,text = "Mostrar gráficos...", font=("Arial", 12), command = self.open_graphic_dialog)
        self.button_show_data.pack(side=BOTTOM, fill=BOTH, padx=100, pady=75)


    def create_menus(self):
        self.menu = Menu()
        # Crear el primer menú.
        self.menu_archivo = Menu(self.menu, tearoff=False)
        self.menu_ayuda = Menu(self.menu, tearoff=False)
        # Agregarlo a la barra.
        self.menu.add_cascade(menu=self.menu_archivo, label="Archivo", underline=0)
        self.menu_archivo.add_command(
            label="Salir",
            accelerator="Ctrl+Q",
            underline=0,
            command=exit
        )
        self.menu.add_cascade(menu=self.menu_ayuda, label="Ayuda", underline=1)
        self.menu_ayuda.add_command(
            label="Acerca de...",
            underline=1,
            command=self.show_info
        )
        self.window.config(background = "white", menu=self.menu)

    
    def create_labels(self):
        # Create a File Explorer label
        self.label_file_explorer = Label(self.window,text = "Ningún fichero seleccionado.", font=("Arial", 12))
        self.label_file_explorer.pack(side=TOP, fill=BOTH, padx=20, pady=20)


    def show_info(self):
        messagebox.showinfo("Acerca de", "License: GNU General Public License v3.0\n\nAuthor: Diego González Suárez - Universidad de Oviedo.\n\nContact Me: uo276406@uniovi.es - diegogs1451@outlook.es\n\nSource Code: https://github.com/uo276406/P48Manager")


    def window_config(self):
        # Set window title
        self.window.title('P48Manager')
        #No redimensionar ventana
        self.window.resizable(width=0, height=0)
        # Set window size
        self.window.geometry("800x400")
        
    # file explorer window
    def parse_file(self):
        self.filename = filedialog.askopenfilename(initialdir = "C:/ESIOS/p48cierre",title = "Seleccione un fichero",filetypes = (("XML files","*.xml*"),("all files","*.*")))
        # Change label contents
        self.label_file_explorer.configure(text="Fichero seleccionado: " + self.filename)
        try:
            self.data = self.parser.parse(self.filename)
        except Exception as e:
            messagebox.showerror("Procesamiento de fichero", e.__str__())
        

    def insert_data(self):
        try:
            number = self.repository.insert(self.data)
            messagebox.showinfo("Operación inserción", "Datos añadidos correctamente: " + str(number) + " filas añadidas")
        except Exception as e:
            messagebox.showerror("Operación de inserción", e.__str__())
    

    def open_graphic_dialog(self):
        GraphicDialog(self.window, self.painter, self.cicles, self.repository)
