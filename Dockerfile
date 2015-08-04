FROM orchardup/python:2.7
ADD . /www
WORKDIR /www
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get -y install libmysqlclient-dev
RUN pip install -r requirements.txt
RUN python manage.py db upgrade
CMD python manage.py runserver -h 0.0.0.0
EXPOSE 5000