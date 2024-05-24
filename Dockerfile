# Use an official Python runtime as the base image
FROM python:3.7.15-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/app

#create log files
RUN mkdir /usr/src/app/logs

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

# Run migrations
#RUN python manage.py makemigrations
#RUN python manage.py migrate

# Run the create_superuser.py script to create the superuser
#RUN python cmd_create_superuser.py

CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]