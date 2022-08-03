import numpy as np
import matplotlib.pyplot as plt

from cicles.P48CierreCicles import P48CierreCicles

class P48CierrePainter():
    def __init__(self, cicles):
        self.cicles = cicles


    def draw(self, data):
        hours = np.arange(1,25,1)
        plt.figure()
        for cicle in self.cicles:
            values = []
            try:
                for hour in hours:
                    values.append(float(data[cicle][hour].replace(',', '.')))
                plt.plot(hours, values, label=cicle, marker='o')
            except KeyError:
                continue
        
        plt.legend(bbox_to_anchor=(1, 1),loc='upper left', borderaxespad=0.)
        plt.grid()
        plt.title('Valores P48Cierre para el día: ' + data['date'])
        plt.xlabel('Horas del día')
        plt.ylabel('MWH')       
        plt.show()