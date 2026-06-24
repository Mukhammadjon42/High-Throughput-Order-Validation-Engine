FROM python:3.10-slim

WORKDIR /app

RUN pip install flask redis 

RUN mkdir -p /var/log/app

COPY app.py .

EXPOSE 9000

CMD ["python", "app.py"]