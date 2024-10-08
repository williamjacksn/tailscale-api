FROM python:3.13-alpine

RUN /usr/sbin/adduser -g python -D python

USER python
RUN /usr/local/bin/python -m venv /home/python/venv

COPY --chown=python:python requirements.txt /home/python/tailscale-api/requirements.txt
RUN /home/python/venv/bin/pip install --no-cache-dir --requirement /home/python/tailscale-api/requirements.txt

ENV PATH="/home/python/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1" \
    TZ="Etc/UTC"

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.source="https://github.com/williamjacksn/tailscale-api"

ENTRYPOINT ["/home/python/venv/bin/python"]

COPY --chown=python:python check-devices.py /home/python/tailscale-api/check-devices.py
COPY --chown=python:python tailscale.py /home/python/tailscale-api/tailscale.py
