# -*- coding:utf8 -*-

from choice import Choices
from django.conf import settings
import repeat
import models

class Sendmail(object):
  name='sendmail'
  def __init__(self,obj):
    self.obj=obj
    self.mailfrom='certificates@gib.loc'
    self.mailto=obj.email.split(';')
    # Объединение self.mailto+obj.group.email+obj.owner.email
    if obj.group.email: self.mailto=set(self.mailto)|set([obj.group.email])
    if obj.owner.email: self.mailto=set(self.mailto)|set([obj.owner.email])
    self.msg=u"""<table>
                 <tr><td>Серийный номер:</td><td>{0}</td></tr>
                 <tr><td>Начало действия:</td><td>{1}</td></tr>
                 <tr><td>Конец действия:</td><td>{2}</td></tr>
                 <tr><td>СКЗИ:</td><td>{3}</td></tr>
                 <tr><td>Группа сертификатов:</td><td>{6}</td></tr>
                 <tr><td>Владелец:</td><td>{7}</td></tr>
                 <tr><td>Издатель:</td><td>{8}</td></tr>
                 <tr><td colspan="2"><a href="http://www.gib.loc/certs/detail/{9}">http://www.gib.loc/certs/detail/{9}</a></td></tr>
                 </table>
              """.format(obj.item,
                         obj.starttime,
                         obj.deadtime,
                         obj.skzi,
                         obj.type,
                         obj.area,
                         obj.group,
                         obj.owner,
                         obj.issuer,
                         obj.pk,
                        )

  def __call__(self):
    from email.MIMEText import MIMEText
    import smtplib
    for mailto in self.mailto:
      try:
        msg=MIMEText(self.msg,'html','utf-8')
        msg['From']=self.mailfrom
        msg['To']=mailto
        msg['Subject']=u'{0} Заканчивается сертификат'.format(self.obj.owner)
        smtp=smtplib.SMTP()
        smtp.connect(settings.SMTP['HOST'],settings.SMTP['PORT'])
        if settings.SMTP['LOGIN']:
          smtp.login(settings.SMTP['LOGIN'],settings.SMTP['PASSWD'])
        smtp.sendmail(self.mailfrom,mailto,msg.as_string())
        smtp.quit()
      except Exception,e:
        import logging
        logger=logging.getLogger(__name__)
        logger.debug('Can`t send email. Reason: %s'%e)

actions=Choices()
actions.register(Sendmail)
