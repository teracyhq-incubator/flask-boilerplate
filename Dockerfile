FROM orchardup/python:2.7
ADD . /www
WORKDIR /www
RUN pip install -r requirements.txt
