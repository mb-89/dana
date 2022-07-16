from dana import gui
from dana.data import datacontainer


def getDatacontainer():
    return datacontainer.Datacontainer()


def showgui(args):
    gui.show(args)
