import matplotlib.pyplot as plt
import numpy as np


class P48CierrePainter:
    def __init__(self, cycles):
        self.cycles = cycles

    def draw(self, data):
        hours = np.arange(1, 25, 1)
        plt.figure()
        for cycle in self.cycles:
            values = []
            try:
                for hour in hours:
                    values.append(float(data[cycle][hour].replace(',', '.')))
                plt.plot(hours, values, label=cycle, marker='o')
            except KeyError:
                continue

        plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
        plt.grid()
        plt.title('Valores P48Cierre para el día: ' + data['date'])
        plt.xlabel('Horas del día')
        plt.ylabel('MWH')
        plt.show()
