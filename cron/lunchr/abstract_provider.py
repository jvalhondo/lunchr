# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import abc
from random import randint
from slackclient import SlackClient


class FoodProvider(object):

    __metaclass__  = abc.ABCMeta

    def __init__(self, service_url):
        self.service_url = service_url
        self.slack_token = os.environ['SLACK_TOKEN']
        self.slack_channel = os.environ['SLACK_CHANNEL']
        self.sc = SlackClient(self.slack_token)
        self.emojis = [
            ':spaghetti:', ':taco:', ':burrito:',
            ':ramen:', ':stew:', ':curry:',
            ':bento:', ':hamburger:', ':sushi:']

    def get_randemoji(self, emojis):
        return emojis[randint(0, len(emojis)-1)]

    @abc.abstractmethod
    def compose_message(self, menu):
        raise NotImplementedError()

    @abc.abstractmethod
    def scrap_menu(self):
        raise NotImplementedError()

    def slack_post_message(self, channel, text, attachments=None):
        attachments = attachments or []
        self.sc.api_call(
            "chat.postMessage", channel=channel, text=text, attachments=attachments)

    def request_menu(self):
        menu = self.scrap_menu()
        if menu:
            message, attachments = self.compose_message(menu)
            self.slack_post_message(
                channel=self.slack_channel,
                text=message,
                attachments=attachments)
