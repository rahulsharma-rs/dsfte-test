#! /usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/dsfet/dsfet')

from dsfet import app as application
#application = create_app()

