FROM ghcr.io/home-assistant/aarch64-base:3.22

RUN apk add --no-cache python3 py3-pip && \
    pip3 install --no-cache-dir --break-system-packages "mcp[cli]<2"

COPY server.py /server.py

CMD ["python3", "/server.py"]
