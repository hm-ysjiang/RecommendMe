import gmmanagar
import wx
from enums import *
import frame


def run():
    gmmanagar.init()

    app = wx.App()
    frame.Frame(SearchTypes)
    app.MainLoop()


if __name__ == '__main__':
    run()
