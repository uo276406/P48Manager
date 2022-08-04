
from tkinter import *
from tkinter import messagebox
import tkcalendar
import datetime



class GraphicDialog():

    def __init__(self, parent, painter, cicles, repository):
 
        self.top = Toplevel(parent)
        self.top.transient(parent)
        self.painter = painter
        self.cicles = cicles
        self.repository = repository
        self.checkboxes = []
        self.checkboxes_values = []
        self.top.grab_set()
        self.top.focus_set()
        self.top.title("P48Manager: Mostrar Gráfico")
        self.top.geometry("1000x650")
        self.top.resizable(width=0, height=0)
        self.cal = self.create_date_picker()
        self.create_checkboxes()
        self.create_buttons()
    
    def create_date_picker(self):
        yesterday_date = datetime.datetime.today() - datetime.timedelta(days=1)
        cal = tkcalendar.Calendar(self.top, selectmode='day', day=yesterday_date.day, month=yesterday_date.month, year=yesterday_date.year)
        cal.pack()
        return cal
    
    def create_checkboxes(self):
        lf = LabelFrame(self.top, text='Ciclos')
        lf.pack(pady = 10)
        column = 0
        row = 0
        for cicle in self.cicles:
            checkbox_value = BooleanVar()
            self.checkboxes_values.append(checkbox_value)
            self.checkboxes.append(Checkbutton(lf,
                text=cicle,
                variable=checkbox_value).grid(row = row, column = column, padx=10, pady=10))
            column += 1
            if column % 10 == 0:
                row += 1
                column = 0

    def create_buttons(self):
        self.button_show_data = Button(self.top ,text = "Limpiar", font=("Arial", 12), command = self.clear_checkboxes)
        self.button_show_data.pack(side=TOP, padx=100, pady=10)
        self.button_show_data = Button(self.top ,text = "Ver datos", font=("Arial", 12), command = self.show_data)
        self.button_show_data.pack(side=TOP, padx=100, pady=10)
        self.button_go_back = Button(self.top,text = "Atrás", font=("Arial", 12), command = self.top.destroy)
        self.button_go_back.pack(side=TOP, padx=100, pady=10)


    def show_data(self):
        datetime_str = self.cal.selection_get().__str__()
        cicles_to_look_for = []
        for i in range(len(self.cicles)):
            if self.checkboxes_values[i].get():
                cicles_to_look_for.append(self.cicles[i])
        
        data = {'date': datetime_str, 'cicles': cicles_to_look_for}
        data = self.repository.find(data)
        show = False
        for cicle in cicles_to_look_for:
            if len(data[cicle]) > 0:
                show = True
        if show:
            self.painter.draw(data)
        else:
            messagebox.showinfo('Ver Datos', 'No se han encontrado datos para el día y los ciclos seleccionados.')

    def clear_checkboxes(self):
        for i in range(len(self.cicles)):
            self.checkboxes_values[i].set(False)
