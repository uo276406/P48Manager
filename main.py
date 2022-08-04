
from gui.MainWindow import MainWindow
from cicles.P48CierreCicles import P48CierreCicles
from painter.P48CierrePainter import P48CierrePainter
from parser.P48CierreParser import P48CierreParser
from repository.P48CierreRepository import P48CierreRepository

# Lista de cicles
cicles = P48CierreCicles()

# Tools
parser = P48CierreParser(cicles)
repository = P48CierreRepository(cicles)
painter = P48CierrePainter(cicles)

try:
    MainWindow(parser, repository, painter, cicles)
except Exception as e:
    print('Ha ocurrido una excepción: ' + e)
    print('Contacte conmigo: diegogs1451@outlook.es')
