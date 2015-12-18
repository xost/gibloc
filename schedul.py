from django.conf import settings
from django.core.wsgi import get_wsgi_application
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gibloc',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'admin',
        'PASSWORD': 'gibloc',
        'HOST': 'jaba.gib.loc',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        #'PORT': '',                      # Set to empty string for default.
    }
}

SMTP={'HOST':'10.0.1.120',
      'PORT':'25',
      'LOGIN':'',
      'PASSWD':'',
      }

settings.configure(DATABASES=DATABASES,SMTP=SMTP)
application = get_wsgi_application()

import django.db.models
import datetime
import tasker.models,tasker.choice,tasker.repeat
import certs.models,certs.choice,certs.repeat

class Tasker(object):
  name=''
  def __call__(self):
    import tasker.repeat as repeat
    for t in tasker.models.Task.objects.all():
      if t.repeat:
        r=tasker.repeat.repeat.get_choice(t.repeat)(t)
        r()
      else:
        pass

class Certs(object):
  name=''
  def __call__(self):
    import certs.repeat as repeat
    for i in certs.models.Cert.objects.all():
      if i.repeat:
        r=certs.repeat.repeat.get_choice(i.repeat)(i)
        r()
      else:
        pass

def main():
  Tasker()()
  Certs()()

if __name__=='__main__':
  main()
