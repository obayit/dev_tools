# -*- coding: utf-8 -*-

import logging
import sys

from odoo import models, fields, api
import odoo

#iessages = []
#iogger = logging.getLogger()

#class FrontLogHandler(logging.StreamHandler):
#    def __init__(self):
#        pass #environment here
#    def emit(self, record):
#        msg = self.format(record)
#        print('############################################################')
#        print(record)
#
#front_handler = FrontLogHandler()  # add log lever from config maybe? even temp/filtered sql stuff may be possible
#front_handler.setLevel(1)
##logger.addHandler(front_handler)
#print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
#
#print('STARTED READING STDOUT')
#while True:
#    print(sys.stdout.read())
#
#print('FINISHED READING STDOUT')

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def do_nothing(self):
        return

