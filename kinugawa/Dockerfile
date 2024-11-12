FROM python:3.12-alpine

WORKDIR /app
COPY index.html .

ENV PORT 3001

CMD python3 -m http.server $PORT
