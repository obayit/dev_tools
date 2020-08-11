# -*- coding: utf-8 -*-
import os
import logging
import threading
import requests
import socket
from contextlib import contextmanager
from threading import Thread
from time import sleep
import json

from odoo import models, fields, api, SUPERUSER_ID
from odoo.tests import common
from odoo import tools, sql_db, http
from odoo.http import request
from odoo.tools import date_utils
import odoo
_logger = logging.getLogger(__name__)  # ironic isn't it?

path_prefix = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
server_address = './odev_log_socket'

def json_dump(v):
    return json.dumps(v, separators=(',', ':'), default=date_utils.json_default)
def environment():
    """ Return an environment with a new cursor for the current database; the
        cursor is committed and closed after the context block.
    """
    registry = odoo.registry(common.get_db_name())
    with registry.cursor() as cr:
        yield odoo.api.Environment(cr, SUPERUSER_ID, {})

class FrontendLoggingController(http.Controller):

    @http.route('/odev_log/', type='http', auth='public', csrf=False)
    def send_stuff(self, message='stuff', **k):
        channel = 'channel4'
        print(channel)
        print('#####################hello world, controller')
        request.env['bus.bus'].sendone(channel, message)
        return ''

class ODevLog(models.AbstractModel):
    _name = "odev.log"
    _description = "Send Log to Frontend"

    @api.model
    def threaded_listener(self):
        pass
        # db_registry = odoo.registry('rsf12')
            # env['bus.bus'].sendone('channel4', 'from thread')
        # with api.Environment.manage(), db_registry.cursor() as cr:
        #     env = api.Environment(cr, SUPERUSER_ID, {})
        #     counter = 3
        #     while counter>0:
        #         # As this function is in a new thread, I need to open a new cursor, because the old one may be closed
        #         print('######################### threaded listener')
        #         print(env)
        #         env['bus.bus'].sendone('channel4', 'from thread')
        #         cr.commit()
        #         print('################ sent')
        #         sleep(1)
        #         counter -= 1
        print('@@@@@@@@@@@@@@@@@@exiting the child thread')

    @api.model
    def start(self):
        try:
            thatSelf = self;

            class FrontendHandler(logging.Handler):
                """ PostgreSQL Logging Handler will store logs in the database, by default
                the current database, can be set using --log-db=DBNAME
                """
                def emit(self, record):
                    ct = threading.current_thread()
                    ct_db = getattr(ct, 'dbname', None)
                    dbname = getattr(ct, 'dbname', None)

                    db_registry = odoo.registry('rsf12')
            # env['bus.bus'].sendone('channel4', 'from thread')
                    with api.Environment.manage(), db_registry.cursor() as cr:
                        env = api.Environment(cr, SUPERUSER_ID, {})
        #     counter = 3
        #     while counter>0:
        #         # As this function is in a new thread, I need to open a new cursor, because the old one may be closed
        #         print('######################### threaded listener')
        #         print(env)
        #         env['bus.bus'].sendone('channel4', 'from thread')
        #         cr.commit()
        #         print('################ sent')
        #         sleep(1)
        #         counter -= 1

                    # with sql_db.db_connect('rsf12', allow_uri=True).cursor() as cr:
                        # As this function is in a new thread, I need to open a new cursor, because the old one may be closed
                        # env = api.Environment(cr, SUPERUSER_ID, {})
                        # preclude risks of deadlocks
                        # cr.execute("SET LOCAL statement_timeout = 1000")
                        msg = tools.ustr(record.msg)
                        if record.args:
                            msg = msg % record.args
                        traceback = getattr(record, 'exc_text', '')
                        if traceback:
                            msg = "%s\n%s" % (msg, traceback)
                        # we do not use record.levelname because it may have been changed by ColoredFormatter.
                        levelname = logging.getLevelName(record.levelno)

                        val = ('server', ct_db, record.name, levelname, msg, record.pathname[len(path_prefix)+1:], record.lineno, record.funcName)
                        if '/longpolling' not in msg:
                            env['bus.bus'].sendone('channel4', json.dumps(val))
                        # sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                        # sock.bind(server_address)
                        #TODO: change port to config parameter
                        # requests.get('http://127.0.0.1:8069/odev_log/',{'message': val}, )

                        # cr.execute("""
                        #     INSERT INTO bus_bus(channel, message)
                        #     VALUES (%s, %s)
                        # """, ['channel4', val])
                        # cr.execute("notify imbus, %s", (json_dump(list('channel4')),))

            #TODO: make sure to run this only once
            frontendHandler = FrontendHandler()
            frontendHandler.setLevel(1)
            logging.getLogger().addHandler(frontendHandler)

            thread = Thread(target = self.threaded_listener)  #  , args = (self, ))
            thread.daemon = True
            print('#############', type(thread))
            thread.start()
            # thread.join()
            print("thread finished...exiting")

            print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ returning from start')
            # request.env['bus.bus'].sendone('channel4', 'trigger notify')
            #print('started odev log #############')
            # self.env.user.notify_success(message='My success message')
            # channel = (self._cr.dbname, 'res.users', self.env.user.id)
        except Exception as ex:
            _logger.warn('Exception happed while starting the {0}, details\n{1}'.format(self._name, str(ex)))