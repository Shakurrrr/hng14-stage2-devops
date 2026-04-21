FROM python:3.12-slim

WORKDIR /app

RUN useradd -m appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

# healthcheck (simple process check)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
CMD pgrep -f worker.py || exit 1

CMD ["python", "worker.py"]