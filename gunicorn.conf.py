import os

bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8000")

workers = int(os.environ.get("GUNICORN_WORKERS", "2"))

workers_class = os.environ.get("GUNICORN_WORKERS_CLASS", "sync")
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "30"))
graceful_timeout = int(os.environ.get("GUNICORN_GRACEFUL_TIMEOUT", "30"))
keepalive = int(os.environ.get("GUNICORN_KEEP_ALIVE", "2"))
loglevel = os.environ.get("LOG_LEVEL", "info").lower()
accesslog = os.environ.get("GUNICORN_ACCESS_LOG", "-")
errorlog = os.environ.get("GUNICORN_ERROR_LOG", "-")
capture_output = True