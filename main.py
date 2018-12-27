import gmmanagar
import json
import kcparser
import wx
from enums import *
import frame as f

api_key_google = kcparser.get_google_api_key()


def run():
    gmmanagar.init(api_key_google)
    # gmmanagar.relocate_center('交通大學')

    app = wx.App()
    frame = f.Frame(SearchTypes)
    app.MainLoop()

    # with open('results.json', 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(gmmanagar.search(1000, type_=SearchTypes.RESTAURANT)
    #                           , indent=4, sort_keys=True, ensure_ascii=False))


if __name__ == '__main__':
    run()
