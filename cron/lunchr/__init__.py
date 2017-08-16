# -*- coding: utf-8 -*-
from __future__ import absolute_import

from lunchr.maragata import Maragata
from lunchr.natsluchbox import NatsLunchbox


class Lunchr(object):

    def feed(self):
        # Maragata provider
        maragata = Maragata(service_url='http://www.lamaragata.com/lamaragata.asp')
        maragata.request_menu()

        # NatsLunchbox provider
        natsluchbox = NatsLunchbox(service_url='http://www.natslunchbox.com/s/cc_images/cache_2471653461.jpg')
        natsluchbox.request_menu()
