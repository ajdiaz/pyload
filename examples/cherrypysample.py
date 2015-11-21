#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

import bottle


@bottle.get('/')
def index():
    return {'key': 'value'}

bottle.run(port=8080, host="0.0.0.0", server="cherrypy")
