
from gui.MainWindow import Window
from cicles.P48CierreCicles import P48CierreCicles
from painter.P48CierrePainter import P48CierrePainter
from parser.P48CierreParser import P48CierreParser
from repository.P48CierreRepository import P48CierreRepository

parser = P48CierreParser()
repository = P48CierreRepository()
painter = P48CierrePainter()
cicles = P48CierreCicles().list
Window(parser, repository, painter, cicles)