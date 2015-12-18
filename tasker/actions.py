from choice import Choices
from django.conf import settings
import repeat
import models

class Sendmail(object):
  name='sendmail'
  def __init__(self,obj):
    self.obj=obj
    self.mailfrom=obj.group.email
    self.mailto=obj.email
    self.msg=u'''<a href="http://www.gib.loc/tasker/detailof/Task/{0}">http://www.gib.loc/tasker/detailof/Task/{0}</a><br/>'''.format(obj.pk)
    self.msg+=u'''<table border='1'>
                 <tr><th>name:</th><td>{0}</td></tr>
                 <tr><th>description:</th><td>{1}</td></tr>
                 <tr><th>state:</th><td>{2}</td></tr>
                 <tr><th colspan='2'>text</th></tr>
                 <tr><td colspan='2'><font color="RED">{3}</font></td></tr>
                 <tr><th>addtime</th><td>{4}</td></tr>
                 <tr><th>deadtime</th><td>{5}</td></tr>
                 <tr><th>repeat</th><td>{6}</td></tr>
                 <tr><th>nday</th><td>{7}</td></tr>
                 <tr><th>owner</th><td>{8}</td></tr>
                 <tr><th>performer</th><td>{9}</td></tr>
                 <tr><th>state</th><td>{10}</td></tr>
                 '''.format(obj.name,
                            obj.description,
                            obj.state,
                            obj.text,
                            obj.addtime,
                            obj.deadtime,
                            repeat.repeat.get_choice(obj.repeat).name,
                            obj.nday,
                            obj.owner,
                            obj.performer,
                            obj.state,
                           )
    self.msg+=u'''<tr><th colspan='2'>comments<th></tr>'''
    for c in models.Comment.objects.filter(task=obj).order_by('-addtime'):
      self.msg+=u'''<tr><th>addtime</th><td>{0}</td></tr>
                    <tr><th>owner</th><td>{1}</td></tr>
                    <tr><td colspan='2'>{2}</td></tr>
                    '''.format(c.addtime,c.owner,c.comment)
    self.msg+='</table>'

  def __call__(self):
    from email.MIMEText import MIMEText
    import smtplib
    try:
      msg=MIMEText(self.msg,'html','utf-8')
      msg['From']=self.mailfrom
      msg['To']=self.mailto
      msg['Subject']='notify:%s'%self.obj
      smtp=smtplib.SMTP()
      smtp.connect(settings.SMTP['HOST'],settings.SMTP['PORT'])
      if settings.SMTP['LOGIN']:
        smtp.login(settings.SMTP['LOGIN'],settings.SMTP['PASSWD'])
      smtp.sendmail(self.mailfrom,self.mailto,msg.as_string())
      smtp.quit()
    except Exception,e:
      print msg['Subject']
      import logging
      logger=logging.getLogger(__name__)
      logger.debug('Can`t send email. Reason: %s'%e)

actions=Choices()
actions.register(Sendmail)
