import geolocation
import gmmanagar
import googlemaps.exceptions
import re
import time
import webbrowser
import widgets
import wx
import wx.html2
import wx.lib.scrolledpanel


class Frame(wx.Frame):

    def __init__(self, enum):
        super().__init__(parent=None, title='Recommend Me!', size=(1000, 500))
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_v1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_h1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_h2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_v2L = wx.BoxSizer(wx.VERTICAL)
        self.sizer_v2R = wx.BoxSizer(wx.VERTICAL)
        self.sizer_h3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_h4 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_v3 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_h5 = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer.Add(self.sizer_v1)
        self.sizer.Add(self.sizer_v3)
        self.sizer_v2L.Add(self.sizer_h3)
        self.sizer_v2L.Add(self.sizer_h4)
        self.sizer_h2.Add(self.sizer_v2L)
        self.sizer_h2.Add(self.sizer_v2R)
        self.sizer_v1.Add(self.sizer_h1)
        self.sizer_v1.Add(self.sizer_h2)

        self.SetSizer(self.sizer)

        # The Search Bar
        self.search_bar = wx.TextCtrl(self, value='Search Here...', size=(180, 25))
        self.sizer_h1.Add(self.search_bar)

        # Radius
        self.radius_pnl = wx.Panel(self)
        self.radius_pnl_sizer = wx.BoxSizer(wx.VERTICAL)
        self.radius_pnl.SetBackgroundColour((171, 171, 171))
        self.radius_pnl.SetSizer(self.radius_pnl_sizer)
        self.radius_pnl_sizer.Add(wx.StaticText(self.radius_pnl, label=' ', size=(80, 5)))
        self.radius_pnl_sizer.Add(wx.StaticText(self.radius_pnl, label='    Radius(m): ', size=(80, 15)))
        self.sizer_h1.Add(self.radius_pnl)
        self.radius_bar = wx.TextCtrl(self, value='1000', size=(45, 25))
        self.sizer_h1.Add(self.radius_bar)

        # The Search Button
        self.search_btn = wx.Button(self, label='Go', size=(80, 25))
        self.search_btn.Bind(wx.EVT_BUTTON, self.on_search)
        self.sizer_h1.Add(self.search_btn)

        # Filters
        self.filter_label_pnl = wx.Panel(self)
        self.filter_label_pnl_sizer = wx.BoxSizer(wx.VERTICAL)
        self.filter_label_pnl.SetBackgroundColour((171, 171, 171))
        self.filter_label_pnl.SetSizer(self.filter_label_pnl_sizer)
        self.filter_label_pnl_sizer.Add(wx.StaticText(self.filter_label_pnl, label=' ', size=(60, 4)))
        self.filter_label_pnl_sizer.Add(wx.StaticText(self.filter_label_pnl, label='Filter by:', size=(60, 25),
                                                      style=wx.ALIGN_CENTER))
        self.checkbox_both = widgets.CheckBox(self, label='Both', size=(50, 25))
        self.checkbox_both.SetValue(True)
        self.checkbox_rank = widgets.CheckBox(self, label='Rank', size=(50, 25))
        self.checkbox_dist = widgets.CheckBox(self, label='Distance', size=(65, 25))
        self.checkbox_hide_closed = wx.CheckBox(self, label='Hide Closed', size=(90, 25))
        self.checkboxes = self.checkbox_both, self.checkbox_rank, self.checkbox_dist
        self.sizer_h3.Add(self.filter_label_pnl, flag=wx.ALIGN_CENTER_VERTICAL)
        self.sizer_h3.Add(self.checkbox_both)
        self.sizer_h3.Add(self.checkbox_rank)
        self.sizer_h3.Add(self.checkbox_dist)
        self.sizer_v2R.Add(self.checkbox_hide_closed)

        # Max Cost
        self.max_cost_pnl = wx.Panel(self)
        self.max_cost_pnl_sizer = wx.BoxSizer(wx.VERTICAL)
        self.max_cost_pnl.SetBackgroundColour((171, 171, 171))
        self.max_cost_pnl.SetSizer(self.max_cost_pnl_sizer)
        self.max_cost_pnl_sizer.Add(wx.StaticText(self.max_cost_pnl, label=' ', size=(60, 3)))
        self.max_cost_pnl_sizer.Add(wx.StaticText(self.max_cost_pnl, label=' ' * 20 + 'Max Cost: ', size=(120, 22)))

        self.sizer_h4.Add(self.max_cost_pnl)
        self.max_cost = wx.TextCtrl(self, size=(45, 22))
        self.sizer_h4.Add(self.max_cost)

        # Macros
        self.macro_list = widgets.MacroScrollPanel(self, (150, 410), enum)
        self.sizer_v2R.Add(self.macro_list)

        # The Result List
        self.results_list = widgets.ResultScrollPanel(self, (235, 381))
        self.sizer_v2L.Add(self.results_list)

        # WebView Panel
        self.web_view_pnl = wx.Panel(self, size=(600, 400))
        self.sizer_v3.Add(self.web_view_pnl)
        self.browser: wx.html2.WebView = wx.html2.WebView.New(self.web_view_pnl, size=(600, 400))
        self.update_browser(gmmanagar.center_id)

        # Open in browser
        self.open = wx.Button(self, size=(600, 30), label='Open In Browser')
        self.sizer_v3.Add(self.open, flag=wx.EXPAND)
        self.open.Bind(wx.EVT_BUTTON, self.open_in_browser)

        # Relocation
        self.sizer_v3.Add(self.sizer_h5)

        self.where_pnl = wx.Panel(self)
        self.where_pnl_sizer = wx.BoxSizer(wx.VERTICAL)
        self.where_pnl.SetBackgroundColour((171, 171, 171))
        self.where_pnl.SetSizer(self.where_pnl_sizer)
        self.where_pnl_sizer.Add(wx.StaticText(self.where_pnl, label=' ', size=(85, 8)))
        self.where_pnl_sizer.Add(wx.StaticText(self.where_pnl, label='   Where am I ?', size=(85, 22)))
        self.sizer_h5.Add(self.where_pnl)

        self.relocate_ip_btn = wx.Button(self, size=(120, 30), label='Relocate Using IP')
        self.relocate_ip_btn.Bind(wx.EVT_BUTTON, self.relocate_ip)
        self.sizer_h5.Add(self.relocate_ip_btn)

        self.or_pnl = wx.Panel(self)
        self.or_pnl_sizer = wx.BoxSizer(wx.VERTICAL)
        self.or_pnl.SetBackgroundColour((171, 171, 171))
        self.or_pnl.SetSizer(self.or_pnl_sizer)
        self.or_pnl_sizer.Add(wx.StaticText(self.or_pnl, label=' ', size=(30, 8)))
        self.or_pnl_sizer.Add(wx.StaticText(self.or_pnl, label='   or', size=(30, 22)))
        self.sizer_h5.Add(self.or_pnl)

        self.relocate_search_btn = wx.Button(self, size=(90, 30), label='Relocate to :')
        self.relocate_search_btn.Bind(wx.EVT_BUTTON, self.relocate_search)
        self.sizer_h5.Add(self.relocate_search_btn)
        self.relocate_search_bar = wx.TextCtrl(self, size=(120, 25))
        self.sizer_h5.Add(self.relocate_search_bar, flag=wx.ALIGN_CENTER_VERTICAL)

        self.or_pnl_2 = wx.Panel(self)
        self.or_pnl_2_sizer = wx.BoxSizer(wx.VERTICAL)
        self.or_pnl_2.SetBackgroundColour((171, 171, 171))
        self.or_pnl_2.SetSizer(self.or_pnl_2_sizer)
        self.or_pnl_2_sizer.Add(wx.StaticText(self.or_pnl_2, label=' ', size=(30, 8)))
        self.or_pnl_2_sizer.Add(wx.StaticText(self.or_pnl_2, label='   or', size=(30, 22)))
        self.sizer_h5.Add(self.or_pnl_2)

        self.relocate_map_btn = wx.Button(self, size=(125, 30), label='According to Map')
        self.relocate_map_btn.Bind(wx.EVT_BUTTON, self.relocate_map)
        self.sizer_h5.Add(self.relocate_map_btn)

        self.Show()

    def on_search(self, event):
        keyword = self.search_bar.GetValue().strip()
        if keyword and keyword != 'Search Here...':
            print('Action performed')
            radius = self.radius_bar.GetValue()
            radius = ''.join([c for c in radius if c.isdigit()])
            self.radius_bar.SetValue(radius)
            max_cost = self.max_cost.GetValue()
            max_cost = ''.join([c for c in max_cost if c.isdigit()])
            self.max_cost.SetValue(max_cost)

            type_ = None
            m = re.search(r'^.*(<.*>)$', keyword)
            if m:
                type_ = m.group(1)[1:len(m.group(1)) - 1]
                keyword = keyword.replace(m.group(1), '')

            if radius:
                kwargs = {'radius': int(radius)}
                if keyword:
                    kwargs['name'] = keyword
                if type_:
                    kwargs['type_'] = type_
                if max_cost:
                    kwargs['max_price'] = int(max_cost)
                if self.checkbox_hide_closed.GetValue():
                    kwargs['open_now'] = True
                print(f'Using args: {kwargs}')
                try:
                    results = []
                    j_places: dict = gmmanagar.search(**kwargs)
                    for result in j_places['results']:
                        d = dict()
                        d['name'] = result['name']
                        d['open_'] = result.get('opening_hours',
                                                None)['open_now'] if result.get('opening_hours', None) else None
                        d['vicinity'] = result.get('vicinity', None)
                        d['rating'] = result.get('rating', None)
                        d['place_id'] = result.get('place_id', None)
                        destination = result['geometry']['location']
                        d['distance'] = gmmanagar.get_distance((destination['lat'], destination['lng']))
                        results.append(d)
                        del d
                    while 'next_page_token' in j_places.keys():
                        kwargs = {'page_token': j_places['next_page_token']}
                        print(f'Using args: {kwargs}')
                        try:
                            time.sleep(5)
                            j_places = gmmanagar.search(**kwargs)
                            for result in j_places['results']:
                                d = dict()
                                d['name'] = result['name']
                                d['open_'] = result.get('opening_hours',
                                                        None)['open_now'] if result.get('opening_hours', None) else None
                                d['vicinity'] = result.get('vicinity', None)
                                d['rating'] = result.get('rating', None)
                                d['place_id'] = result.get('place_id', None)
                                destination = result['geometry']['location']
                                d['distance'] = gmmanagar.get_distance((destination['lat'], destination['lng']))
                                results.append(d)
                                del d
                        except googlemaps.exceptions.ApiError as e:
                            if e.status == 'INVALID_REQUEST':
                                break
                        except googlemaps.exceptions.Timeout:
                            print('Timeout on searching!')
                            break

                    print('End searching, sorting results')
                    if self.checkbox_both.GetValue():
                        pass
                    elif self.checkbox_dist.GetValue():
                        results = sorted(results, key=lambda e: int(self.radius_bar.GetValue()) - e['distance'] * 1000,
                                         reverse=True)
                    elif self.checkbox_rank.GetValue():
                        results = sorted(results, key=lambda e: e['rating'] if e['rating'] else 0, reverse=True)
                    self.results_list.set_results(results)
                    self.results_list.update_results()
                except googlemaps.exceptions.Timeout:
                    print('Timeout on searching!')

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
        if self.checkbox_both.GetValue():
            pass
        elif self.checkbox_dist.GetValue():
            self.results_list.results = sorted(self.results_list.results,
                                               key=lambda e: int(self.radius_bar.GetValue()) - e['distance'] * 1000,
                                               reverse=True)
        elif self.checkbox_rank.GetValue():
            self.results_list.results = sorted(self.results_list.results,
                                               key=lambda e: e['rating'] if e['rating'] else 0, reverse=True)
        self.results_list.update_results()

    def on_checkout(self, event):
        for result in self.results_list.pnl_list:
            if result.btn.Id == event.Id:
                self.update_browser(result.place_id)

    def open_in_browser(self, event):
        print(f'Open URL: {self.browser.GetCurrentURL()}')
        webbrowser.open(self.browser.GetCurrentURL())

    def update_browser(self, id_=None):
        if id_:
            self.browser.LoadURL(f'https://www.google.com/maps/place/?q=place_id:{id_}')
        else:
            self.browser.LoadURL(f'https://www.google.com/maps/place/?q={gmmanagar.center[0]},{gmmanagar.center[1]}')

    def relocate_ip(self, event):
        gmmanagar.relocate_center_latlng(*geolocation.get_location(geolocation.get_ip()))
        self.update_browser()

    def relocate_search(self, event):
        print(self.relocate_search_bar.GetValue())
        if self.relocate_search_bar.GetValue():
            try:
                gmmanagar.relocate_center_query(self.relocate_search_bar.GetValue().split(' '))
                print(gmmanagar.center)
                self.update_browser()
            except googlemaps.exceptions.Timeout:
                print('Timeout on relocating')

    def relocate_map(self, event):
        print(self.browser.GetCurrentURL())
        m = re.search(r'^https://www.google.com/maps/place/'
                      r'(\?q=place_id:(.+))?(.+/@([-\d\.]+,[-\d\.]+),\d+z.*)?$',
                      self.browser.GetCurrentURL())
        if m:
            if m.group(4) is None:
                gmmanagar.relocate_center_place_id(m.group(2))
            else:
                gmmanagar.relocate_center_latlng(*m.group(4).split(','))
            self.update_browser()
