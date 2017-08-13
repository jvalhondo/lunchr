# -*- coding: utf-8 -*-
from __future__ import absolute_import

import requests

from datetime import datetime
from bs4 import BeautifulSoup

from .abstract_provider import FoodProvider


class Maragata(FoodProvider):

    name = 'maragata'

    def scrap_menu(self):
        # Get daily menu
        r = requests.get(self.service_url)
        # init bs4 parser
        soup = BeautifulSoup(r.content, "html.parser")
        # define target table attrs
        _table_attrs = dict(align='center', border='0',
                            cellspacing='0', width='100%')
        # lookup for target tables
        tables = soup.find_all('table', attrs=_table_attrs)

        def _table_parser(table):
            rows = table.find_all('tr')
            data = list()
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip().lower()
                        for ele in cols]
                # Get rid of empty values
                data.append([ele for ele in cols if ele])

            return sum(data, list())[1:]

        # build menu dict & timestamp
        if tables:
            menu = dict(primer_plato=_table_parser(tables[0]),
                        segundo_plato=_table_parser(tables[1]),
                        fecha=str(datetime.today().date()),
                        telefono='91 564 44 82')
            return menu

        return dict()

    def compose_message(self, menu):
        attachments = []

        def compose_items(data):
            _message = ""
            for item in data:
                _message += '   - ' + item + '\n'
            return _message

        # compose 2 random emojis
        message = self.get_randemoji(emojis=self.emojis) + \
            self.get_randemoji(emojis=self.emojis) + \
            ' *Menú Maragata:* \n'
        # compose 'primer plato'
        message += '*Primer Plato:* ' + '\n' + compose_items(
            menu['primer_plato'])
        # compose 'segundo plato'
        message += '*Segundo Plato:* ' + '\n' + compose_items(
            menu['segundo_plato'])
        # compose 'fecha'
        message += '*Fecha:* ' + menu['fecha'] + '\n'
        # compose 'telefono'
        message += '*Telefono:* ' + menu['telefono'] + '\n'

        return message, attachments
