# -*- coding: utf-8 -*-

# 1) Linkero Core
import linkero.core.linkero as linkero
#import linkero.core.gateway.gevent_service as gevent
#import core.gateway.waitress_service as waitress

# 2) APIs developed to use with Linkero
import api

# 3) Load desired APIs
api.loadRaijinAPI()

# 4) Run Linkero
linkero.run()
#gevent.run(linkero.app)
#waitress.run(linkero.app)
