"""
    Project available: https://github.com/uo276406/P48Manager
    @author: Diego González Suárez - diegogs1451@outloo.es
"""

from cycles.P48CierreCicles import P48CierreCycles
from gui.MainWindow import MainWindow
from painter.P48CierrePainter import P48CierrePainter
from parser.P48CierreParser import P48CierreParser
from repository.P48CierreRepository import P48CierreRepository

# Lista de ciclos
cycles = P48CierreCycles().list

# Tools
parser = P48CierreParser(cycles)
repository = P48CierreRepository(cycles)
painter = P48CierrePainter(cycles)

try:
    MainWindow(parser, repository, painter, cycles)
except Exception as e:
    print('Ha ocurrido una excepción: ' + e.__str__())
    print('Contacte conmigo: diegogs1451@outlook.es')
