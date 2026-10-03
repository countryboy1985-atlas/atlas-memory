FROM ghcr.io/home-assistant/aarch64-base:3.22

RUN apk add --no-cache python3 py3-flask

COPY server.py /server.py

CMD ["python3", "/server.py"]
