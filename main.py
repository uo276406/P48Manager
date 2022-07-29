from gui.window import Window
from parser.p48parser import p48parser
from repository.p48repository import p48repository

parser = p48parser()
repository = p48repository()
Window(parser, repository)