import gmmanagar
import wx
import frame


def run():
    gmmanagar.init()

    app = wx.App()
    frame.Frame()
    app.MainLoop()


if __name__ == '__main__':
    run()
