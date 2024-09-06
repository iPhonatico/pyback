# Pull the image from Dockerhub
FROM python:alpine3.19

RUN mkdir /code
WORKDIR /code

# set up python environment variables

ENV PYTHONDOWNWRITEBYTECODE 1
ENV PYTHONNUNBUFFER 1

# update and  install dependencies
RUN pip install --upgrade pip
ADD requierements.txt /code/requierements.txt
RUN pip install -r requierements.txt

# copy project
ADD . /code/

# Expose the port server is running on
EXPOSE 8000
