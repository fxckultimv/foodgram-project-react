FROM python:3.9

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]

# для локального запуска использовал ["python", "manage.py", "runserver", "0:8000"]
