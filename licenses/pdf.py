#!/usr/bin/python
# -*- coding: utf-8 -*-

from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Spacer,Paragraph
from reportlab.lib.enums import TA_JUSTIFY,TA_RIGHT,TA_CENTER
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class Report(object):

  def __init__(self,*args,**kwargs):
    print '__init__'
    return super(Report,self).__init__(*args,**kwargs)

def main():
  doc=SimpleDocTemplate('pdf.pdf')
  pdfmetrics.registerFont(TTFont('Arial','arial.ttf'))
  styles=getSampleStyleSheet()
  styles.add(ParagraphStyle('H1',parent=styles['Heading2'],alignment=TA_CENTER,fontName="Arial"))
  styles.add(ParagraphStyle('NormalText',parent=styles['Normal'],alignment=TA_JUSTIFY,fontName="Arial"))
  text1='Акт передачи<br/>на использование программного продукта Крипто-Про CSP 3.6'
  text2="""Настоящий акт действует в рамках Лицензионного соглашение с ООО \"Крипто-Про\" и Пользователем (физическим или юридическим лицом).<br/><br/>
  Настоящая лицензия даёт право на утановку и использование одной копии Изделия (программного продукта) %s в составе программного обеспечения \"ИНИСТ Банк-Клиент\"
  используемого \"Гранд Инвест Банк\" (ОАО), в соответствии с Лицензионным соглашением и правилами пользования, изложенными в эксплуатационной документации.<br/><br/>
  \"Гранд Инвест Банк\" (ОАО) передаёт настоящую лицензию на условиях использования только в составе программного обеспечения \"ИНИСТ Банк-Клиент\".<br/><br/>
  Ответственность за использование настоящей лицензии в составе иных программных продуктов несёт пользователь.""" % ('CryptoPro CSP 3.6')
  p1=Paragraph(text1,styles['H1'])
  p2=Paragraph(text2,styles['NormalText'])
  space=Spacer(0,inch)
  Story=[p1,space,p2]
  doc.build(Story)

if __name__=='__main__':
  main()
