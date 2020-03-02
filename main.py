import requests
from bs4 import BeautifulSoup
import time
from PIL import Image
import numpy as np
from xhtml2pdf import pisa
#import matplotlib.pyplot as plt
import requests
from io import BytesIO
#import pdfkit
import os
import pytesseract
template='''<html>
    <head>
        <title>
            GTU RESULT
        </title>
        <style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 12px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style></head><body><table><tr><th>Enrollment No:</th><th>CPI</th></tr>'''
templatelast="</table><h5>Prepared by OverclockedBrains</h5><h5>This PDF is genrated by GTUResult-Bot...<br>This project is opensource, For source code visit:<br><a href='https://github.com/ssd39/GTUResult-Bot'>https://github.com/ssd39/GTUResult-Bot</a></h5></body></html>"

def convertHtmlToPdf(sourceHtml, outputFilename):
    resultFile = open(outputFilename, "w+b")
    pisaStatus = pisa.pip3 (sourceHtml,resultFile)
    resultFile.close()
    return pisaStatus.err

while True:
    d=requests.get("https://www.gturesults.in/")
    soup = BeautifulSoup(d.text,'lxml')
    subject_options = [i.findAll('option') for i in soup.findAll('select', attrs={'name': 'ddlbatch'})]
    a = str(subject_options[0]).find('BE SEM 5')
    if (a != -1):
        break

option_value = str(subject_options[0])[a-38:a-7]
enprefixo="170410107"
for iot in range(1,12):
    for djfhui in range(0,5):
        enprefix=""+enprefixo
        s = requests.Session()
        d = s.get('https://www.gturesults.in/')
        soup = BeautifulSoup(d.text,'lxml')
        subject_options = [i.findAll('option') for i in soup.findAll('select', attrs={'name': 'ddlbatch'})]
        a = str(subject_options[0]).find('BE SEM 5')
        option_value = str(subject_options[0])[a - 38:a - 7]
        __VIEWSTATE=soup.select_one('#__VIEWSTATE').get('value')
        #__EVENTTARGET=soup.select_one('#__EVENTTARGET').get('value')
        #__EVENTARGUMENT=soup.select_one('#__EVENTARGUMENT').get('value')
        __VIEWSTATEGENERATOR=soup.select_one('#__VIEWSTATEGENERATOR').get('value')
        if iot >99:
            enprefix+=str(iot)
        elif iot <10:
            enprefix+=str(0)+str(0)+str(iot)
        else:
            enprefix+=str(0)+str(iot)
        image_from_gtu = s.get("http://gturesults.in/Handler.ashx")
        i = Image.open(BytesIO(image_from_gtu.content))
        iar = np.asarray(i)
        iar = np.delete(iar, 23, 0)
        img = Image.fromarray(iar, 'RGB')
        textotp = pytesseract.image_to_string(img)
        #print(textotp)
        #print(enprefix)
        payload={"__EVENTTARGET":"","__EVENTARGUMENT":"","__VIEWSTATE":__VIEWSTATE,"__VIEWSTATEGENERATOR":__VIEWSTATEGENERATOR,"ddlbatch":option_value,"txtenroll":enprefix,"txtSheetNo":"","CodeNumberTextBox":textotp,"btnSearch":"Search"}
        l=s.post("https://www.gturesults.in/",data=payload)
        soupx = BeautifulSoup(l.text, 'lxml')
        #f=open("{}.html".format(iot),"w")
        #f.write(l.text)
        #f.close()
        resultol=soupx.select_one('#lblmsg').text
        #print(resultol)
        if resultol:
            assd=resultol.split(" ")
            if assd[0]=="Congratulation!!" or assd[0]=="Sorry!":
                cpi=soupx.select_one('#lblCPI').text
                template+="<tr><td>{}</td><td>{}</td></tr>".format(enprefix,cpi)
                print(enprefix,cpi)
                break

template+=templatelast
f=open("lol.html","w")
f.write(template)
f.close()

#pdfkit.from_file('lol.html', 'GTU.pdf')
#pisa.showLogging()
#convertHtmlToPdf(templatelast, "GTU.pdf")

os.popen("weasyprint lol.html gtu.pdf").readlines()

