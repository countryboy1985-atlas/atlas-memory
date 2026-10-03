ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache python3 py3-flask

COPY server.py /server.py

CMD ["python3", "/server.py"]
