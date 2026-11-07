# Self-hosted image (Vercel does not use this file).
#
#   docker build -t progressbar .
#   docker run --rm -p 127.0.0.1:8099:8099 progressbar
#
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PROGRESSBAR_BIND=0.0.0.0:8099

WORKDIR /app

# requirements.txt is a pip-compile lock file (every package pinned + hashed),
# and only wheels are accepted, so nothing is built from source at image time.
COPY requirements.txt ./
RUN pip install --require-hashes --only-binary :all: -r requirements.txt

COPY app.py gunicorn.conf.py ./
COPY templates ./templates

RUN useradd --system --uid 10001 --no-create-home progressbar
USER progressbar

EXPOSE 8099

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import sys, urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8099/health', timeout=2).status == 200 else 1)"

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
