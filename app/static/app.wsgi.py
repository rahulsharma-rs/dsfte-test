import sys
sys.path.insert(0, '/var/www/html/dashboards')

from flaskr import create_app
application = create_app()
print('x')