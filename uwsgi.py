# coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pachong_webservice.settings")

application = get_wsgi_application()
