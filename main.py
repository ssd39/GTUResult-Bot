from bs4 import BeautifulSoup
from PIL import Image
import numpy as np
import requests
from io import BytesIO
import os
import pytesseract
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
from flask import Flask
import threading
import time

def cronwork():
    while True:
        time.sleep(8)
        a=requests.get("https://gturesult.herokuapp.com/")

def mainwork():
    template='''<html><head><title>GTU RESULT</title><style>
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



    while True:
        time.sleep(8)
        d=requests.get("https://www.gturesults.in/")
        soup = BeautifulSoup(d.text,'lxml')
        subject_options = [i.findAll('option') for i in soup.findAll('select', attrs={'name': 'ddlbatch'})]
        a = str(subject_options[0]).find('BE SEM 3')
        if (a != -1):
            break

    option_value = str(subject_options[0])[a-38:a-7]
    enprefixo="180410107"
    for iot in range(1,131):
        for djfhui in range(0,5):
            enprefix=""+enprefixo
            s = requests.Session()
            d = s.get('https://www.gturesults.in/')
            soup = BeautifulSoup(d.text,'lxml')
            subject_options = [i.findAll('option') for i in soup.findAll('select', attrs={'name': 'ddlbatch'})]
            a = str(subject_options[0]).find('BE SEM 3')
            option_value = str(subject_options[0])[a - 38:a - 7]
            __VIEWSTATE=soup.select_one('#__VIEWSTATE').get('value')
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
            payload={"__EVENTTARGET":"","__EVENTARGUMENT":"","__VIEWSTATE":__VIEWSTATE,"__VIEWSTATEGENERATOR":__VIEWSTATEGENERATOR,"ddlbatch":option_value,"txtenroll":enprefix,"txtSheetNo":"","CodeNumberTextBox":textotp,"btnSearch":"Search"}
            l=s.post("https://www.gturesults.in/",data=payload)
            soupx = BeautifulSoup(l.text, 'lxml')
            resultol=soupx.select_one('#lblmsg').text
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


    os.popen("weasyprint lol.html gtu.pdf").readlines()



    message = Mail(
        from_email='gtubot@ob.com',
        to_emails='saurabh.sachit39@gmail.com',
        subject='GTU RESULT BOT',
        html_content='<strong>GTU Result is now available</strong>'
    )

    with open('gtu.pdf', 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName('GTUResult.pdf'),
        FileType('application/pdf'),
        Disposition('attachment')
    )
    message.attachment = attachedFile

    sg = SendGridAPIClient("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")
    response = sg.send(message)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World from Flask"

if __name__ == "__main__":
    # Only for debugging while developing
    t1 = threading.Thread(target=mainwork)
    t2 = threading.Thread(target=cronwork)
    t1.start()
    t2.start()
    print("Flask API started")
    app.run(host='0.0.0.0', debug=True, port=os.environ['PORT'])
