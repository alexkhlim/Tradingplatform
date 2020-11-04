FROM python:3

COPY . /app
WORKDIR /app
RUN pip install -r requariments.txt
CMD python manage.py runserver 0.0.0.0:8000