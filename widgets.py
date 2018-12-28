import wx
import wx.lib.scrolledpanel


class ScrollPanel(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, parent, size):
        super().__init__(parent=parent, size=size)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetSizer(self.sizer)
        self.SetupScrolling(False, True, rate_x=10)


class MacroScrollPanel(ScrollPanel):
    def __init__(self, parent, size, enum):
        super().__init__(parent=parent, size=size)
        self.btn_list = []

        for e in enum:
            btn = wx.Button(self, size=(133, 40), label=e.value)
            btn.Bind(wx.EVT_BUTTON, parent.on_macro_selected)
            self.btn_list.append(btn)
            self.sizer.Add(btn)


class ResultPanel(wx.Panel):
    def __init__(self, parent, size, name, open_, vicinity, rating, distance, place_id):
        super().__init__(parent=parent, size=size)
        self.SetBackgroundColour((204, 204, 204))
        self.name = name
        self.open = open_
        self.vicinity = vicinity
        self.rating = rating
        self.distance = distance
        self.place_id = place_id

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer_h1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_h2 = wx.BoxSizer(wx.HORIZONTAL)

        # extra space
        self.sizer.Add(wx.StaticText(self, label='', size=(10, 5)))

        self.sizer_h1.Add(wx.StaticText(self, label=('  '+self.name), size=(150, 15)),
                          flag=wx.ALIGN_CENTER_VERTICAL)
        self.sizer_h1.Add(wx.StaticText(self, label='Open  ' if self.open else 'Closed',
                                        size=(68, 15), style=wx.ALIGN_RIGHT))
        self.sizer.Add(self.sizer_h1)

        self.sizer.Add(wx.StaticText(self, label=('  '+self.vicinity), size=(218, 15)), flag=wx.ALIGN_CENTER_VERTICAL)

        # extra space
        self.sizer.Add(wx.StaticText(self, label='', size=(10, 5)))

        self.btn = wx.Button(self, label='Check out', size=(180, 20))
        self.btn.Bind(wx.EVT_BUTTON, self.on_checkout)
        self.sizer.Add(self.btn, flag=wx.ALIGN_CENTER)

        # extra space
        self.sizer.Add(wx.StaticText(self, label='', size=(10, 5)))

        self.sizer_h2.Add(wx.StaticText(self, label=('  Rating: ' + str(self.rating)), size=(120, 15)))
        self.sizer_h2.Add(wx.StaticText(self, label=('Distance: ' + str(self.distance)) + '  ', size=(100, 15),
                                        style=wx.ALIGN_RIGHT),
                          flag=wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add(self.sizer_h2)

        self.SetSizer(self.sizer)

    def on_checkout(self, event):
        print(f'{self.name}: {self.place_id}')


class ResultScrollPanel(ScrollPanel):
    def __init__(self, parent, size):
        super().__init__(parent=parent, size=size)
        self.pnl_list = []

    def update_results(self, results):
        del self.pnl_list
        self.pnl_list = []
        self.sizer.Clear(True)
        for result in results:
            pnl = ResultPanel(self, size=(218, 85), **result)
            self.pnl_list.append(pnl)
            self.sizer.Add(pnl)
            self.sizer.AddSpacer(3)
        self.sizer.Add(wx.StaticText(self, label='------End Of Data------', size=(240, 25), style=wx.ALIGN_CENTER))
        self.SetupScrolling(False, True, rate_x=10)


class CheckBox(wx.CheckBox):
    def __init__(self, parent, label, size):
        super().__init__(parent=parent, label=label, size=size)
        self.Bind(wx.EVT_CHECKBOX, parent.on_checkbox_clicked)
