FROM python:3.7
WORKDIR /code

RUN  chmod -R g+rws  /code

# RUN  mkdir -p /pipcache 
# RUN  chown -R "0:33"  /rootzzz
# USER "0:33"

ADD requirements.txt /code/
RUN pip install  -r requirements.txt

# use volume in docker-compose..
# COPY . /code/


