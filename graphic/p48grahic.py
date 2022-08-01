import numpy as np
import matplotlib.pyplot as plt

from cicles.p48cicles import P48cicles

class P48grapic():
    def draw(self, data):
        hours = np.arange(1,25,1)
        plt.figure()
        for cicle in P48cicles().list:
            values = []
            try:
                for hour in hours:
                    values.append(data[cicle][hour])
                plt.plot(hours, values, label=cicle, marker='o')
            except KeyError:
                continue
        
        plt.legend(bbox_to_anchor=(1, 1),loc='upper left', borderaxespad=0.)
        plt.grid()
        plt.title('Valores P48Cierre para el día: ' + data['date'])
        plt.xlabel('Horas del día')
        plt.ylabel('MWH')       
        plt.show()