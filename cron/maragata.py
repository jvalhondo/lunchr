import os
import urllib.request
from datetime import datetime
from random import randint
from bs4 import BeautifulSoup
from slackclient import SlackClient


class Maragata(object):

    def __init__(self):
        self.maragata_url = 'http://www.lamaragata.com/lamaragata.asp'
        self.slack_token = os.environ['SLACK_TOKEN']
        self.slack_channel = os.environ['SLACK_CHANNEL']
        self.sc = SlackClient(self.slack_token)

    def scrap_menu(self, r):
        # init bs4 parser
        soup = BeautifulSoup(r, "html.parser")
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
        message = ""
        emojis = [':spaghetti:', ':taco:', ':burrito:',
                  ':ramen:', ':stew:', ':curry:',
                  ':bento:', ':hamburger:', ':sushi:']

        def compose_items(data):
            _message = ""
            for item in data:
                _message += '   - ' + item + '\n'
            return _message

        def get_randemoji(emojis):
            return emojis[randint(0, len(emojis)-1)]

        # compose 2 random emojis
        message += get_randemoji(
            emojis=emojis) + get_randemoji(emojis=emojis) + '\n'
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

        return message

    def slack_post_message(self, channel, text):
        self.sc.api_call("chat.postMessage", channel=channel, text=text)

    def request_menu(self):
        r = urllib.request.urlopen(self.maragata_url).read()

        menu = self.scrap_menu(r=r)

        if menu:
            self.slack_post_message(channel=self.slack_channel,
                                    text=self.compose_message(menu))


maragata = Maragata()
maragata.request_menu()
