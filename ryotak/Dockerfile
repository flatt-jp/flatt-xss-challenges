FROM python:3.12-alpine

WORKDIR /app

COPY index.html .
COPY server.py .

CMD python3 server.py $PORT
