FROM tiangolo/uwsgi-nginx-flask:python3.7


RUN pip3 install pillow && \
    pip3 install bs4 && \
    pip3 install numpy && \
    pip3 install requests && \
    pip3 install lxml && \
    pip3 install pytesseract && \
    pip3 install weasyprint && \
    pip3 install sendgrid 

RUN  apt-get update && \
     apt-get install tesseract-ocr -y

COPY main.py ./main.py

CMD python3 main.py
