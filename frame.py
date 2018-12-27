import gmmanagar
import googlemaps.exceptions
import re
import widgets
import wx
import wx.lib.scrolledpanel


class Frame(wx.Frame):

    def __init__(self, enum):
        super().__init__(parent=None, title='Recommend Me!', size=(400, 500))
        self.sizer_v1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_h1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_h2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_v2L = wx.BoxSizer(wx.VERTICAL)
        self.sizer_v2R = wx.BoxSizer(wx.VERTICAL)
        self.sizer_h3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_h4 = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer_v2L.Add(self.sizer_h3)
        self.sizer_v2L.Add(self.sizer_h4)
        self.sizer_h2.Add(self.sizer_v2L)
        self.sizer_h2.Add(self.sizer_v2R)
        self.sizer_v1.Add(self.sizer_h1)
        self.sizer_v1.Add(self.sizer_h2)

        # The Search Bar
        self.search_bar = wx.TextCtrl(self, value='Search Here...', size=(200, 25))
        self.sizer_h1.Add(self.search_bar)

        # Radius
        self.radius_pnl = wx.Panel(self)
        self.radius_pnl_sizer = wx.BoxSizer(wx.VERTICAL)
        self.radius_pnl.SetSizer(self.radius_pnl_sizer)
        self.radius_pnl_sizer.Add(wx.StaticText(self.radius_pnl, label=' Radius(m): ', size=(65, 25)))
        self.sizer_h1.Add(self.radius_pnl)
        self.radius_bar = wx.TextCtrl(self, value='1000', size=(45, 25))
        self.sizer_h1.Add(self.radius_bar)

        # The Search Button
        self.search_btn = wx.Button(self, label='Go', size=(80, 25))
        self.search_btn.Bind(wx.EVT_BUTTON, self.on_search)
        self.sizer_h1.Add(self.search_btn)
        self.SetSizer(self.sizer_v1)

        # Filters
        self.filter_label = wx.StaticText(self, label='Filter by:', size=(60, 25), style=wx.ALIGN_CENTER)
        self.checkbox_both = widgets.CheckBox(self, label='Both', size=(50, 25))
        self.checkbox_both.SetValue(True)
        self.checkbox_rank = widgets.CheckBox(self, label='Rank', size=(50, 25))
        self.checkbox_dist = widgets.CheckBox(self, label='Distance', size=(65, 25))
        self.checkbox_hide_closed = wx.CheckBox(self, label='Hide Closed', size=(90, 25))
        self.checkboxes = self.checkbox_both, self.checkbox_rank, self.checkbox_dist
        self.sizer_h3.Add(self.filter_label, flag=wx.ALIGN_CENTER_VERTICAL)
        self.sizer_h3.Add(self.checkbox_both)
        self.sizer_h3.Add(self.checkbox_rank)
        self.sizer_h3.Add(self.checkbox_dist)
        self.sizer_v2R.Add(self.checkbox_hide_closed)

        # Max Cost
        self.sizer_h4.Add(wx.StaticText(self, label=' '*20+'Max Cost: ', size=(120, 22)))
        self.max_cost = wx.TextCtrl(self, size=(45, 22))
        self.sizer_h4.Add(self.max_cost)

        # Macros
        self.macro_list = widgets.MacroScrollPanel(self, (165, 410), enum)
        self.sizer_v2R.Add(self.macro_list)

        # The Result List
        self.results = widgets.ResultScrollPanel(self, (235, 410))
        self.sizer_v2L.Add(self.results)

        self.Show()

    def on_search(self, event):
        keyword = self.search_bar.GetValue().strip()
        if keyword and keyword != 'Search Here...':
            radius = self.radius_bar.GetValue()
            radius = ''.join([c for c in radius if c.isdigit()])
            self.radius_bar.SetValue(radius)
            max_cost = self.max_cost.GetValue()
            max_cost = ''.join([c for c in max_cost if c.isdigit()])
            self.max_cost.SetValue(max_cost)

            type_ = None
            m = re.search(r'^.*(<.*>)$', keyword)
            if m:
                type_ = m.group(1)[1:len(m.group(1))-1]
                keyword = keyword.replace(m.group(1), '')

            if radius:
                kwargs = {}
                if keyword:
                    kwargs['name'] = keyword
                if type_:
                    kwargs['type_'] = type_
                if max_cost:
                    kwargs['max_price'] = int(max_cost)
                if self.checkbox_hide_closed.GetValue():
                    kwargs['open_now'] = True
                try:
                    j_places = gmmanagar.search(int(radius), **kwargs)
                    # print(json.dumps(j_places, indent=4))
                    results = []
                    for result in j_places['results']:
                        d = dict()
                        d['name'] = result['name']
                        d['open_'] = result.get('opening_hours',
                                                None)['open_now'] if result.get('opening_hours', None) else None
                        d['vicinity'] = result.get('vicinity', None)
                        d['rating'] = result.get('rating', None)
                        d['place_id'] = result.get('place_id', None)
                        d['distance'] = 0
                        results.append(d)
                        del d
                    self.results.update_results(results)
                except googlemaps.exceptions.Timeout:
                    print('Timeout!')

    def on_macro_selected(self, event):
        for btn in self.macro_list.btn_list:
            if btn.Id == event.Id:
                keyword: str = self.search_bar.GetValue().strip()
                if keyword == 'Search Here...':
                    keyword = ''
                m = re.search(r'^.*<(.*)>$', keyword)
                if m:
                    keyword = keyword.replace(m.group(1), btn.Label)
                else:
                    keyword += f'<{btn.Label}>'
                self.search_bar.SetValue(keyword)

    def on_checkbox_clicked(self, event):
        for box in self.checkboxes:
            box.SetValue(box is event.GetEventObject())
