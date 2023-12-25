# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Set the working directory to /code
WORKDIR /home

# create root directory for our project in the container
RUN mkdir /project

WORKDIR /home/project

RUN pip install --upgrade pip



COPY requirements.txt /home/project/
# Install any needed packages specified in requirements.txt

RUN pip install -r requirements.txt

COPY . /home/project/

COPY ./entrypoint.sh /home/project

ENTRYPOINT [ "sh" ,"entrypoint.sh" ]