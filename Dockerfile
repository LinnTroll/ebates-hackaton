FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update && apt-get install -y mysql-client && rm -rf /var/lib/apt
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
