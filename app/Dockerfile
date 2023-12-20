FROM python:3.9.18-alpine3.17


WORKDIR /app

COPY . . 

RUN python3 -m venv venv && . venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt

RUN python3 manage.py collectstatic --no-input
RUN python3 manage.py migrate

EXPOSE 8000

CMD [ "/bin/sh", "-c", "python3 manage.py runserver 0.0.0.0:8000" ]