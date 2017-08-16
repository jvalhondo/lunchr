# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datetime import date

from .abstract_provider import FoodProvider


class NatsLunchbox(FoodProvider):

    name = 'natslunchbox'

    def scrap_menu(self):
        return self.service_url

    def compose_message(self, menu):
        # compose 2 random emojis
        message = self.get_randemoji(emojis=self.emojis) + \
            self.get_randemoji(emojis=self.emojis) + \
            ' *Menú Nat\'s Lunchbox:* \n'
        # compose 'fecha'
        message += '*Fecha:* ' + date.today().strftime("%Y-%m-%d") + '\n'
        # compose 'telefono'
        message += '*Telefono:* 91 009 25 44\n'

        attachments = [{
            'title': 'NatsLunchbox menu',
            'image_url': menu
        }]

        return message, attachments
