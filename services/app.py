import importlib
import argparse

from zmq.eventloop import ioloop

from baselayer.app import cfg
from baselayer.app.app_server import (handlers as baselayer_handlers,
                                      settings as baselayer_settings)

import tornado.log

ioloop.install()

parser = argparse.ArgumentParser(description='Launch webapp')
parser.add_argument('--config', action='append')
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()

if args.config:
    for config in args.config:
        cfg.update_from(config)

app_factory = cfg['app:factory']
baselayer_settings['cookie_secret'] = cfg['app:secret-key']
baselayer_settings['autoreload'] = args.debug

module, app_factory = app_factory.rsplit('.', 1)
app_factory = getattr(importlib.import_module(module), app_factory)

app = app_factory(cfg, baselayer_handlers, baselayer_settings)
app.cfg = cfg

app.listen(cfg['app:port'])

ioloop.IOLoop.current().start()
