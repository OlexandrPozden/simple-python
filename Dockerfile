FROM python:3

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./backend /app/backend
COPY ./app.py /app/
COPY ./app.ini /app/
WORKDIR /app

CMD ["uwsgi","app.ini"]
