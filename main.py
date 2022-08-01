from gui.window import Window
from parser.p48parser import P48parser
from repository.p48repository import P48repository
from graphic.p48grahic import P48grapic

parser = P48parser()
repository = P48repository()
graphic = P48grapic()
Window(parser, repository, graphic)