FROM python:3.7

RUN apt-get update
RUN apt-get upgrade -y

# App code will be deployed into /app within docker container
WORKDIR /src
ADD . /src

# Add and install Python modules.  Note additional uwsgi install, required to make app windows compatible
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#CMD bash
CMD python app/location.py
