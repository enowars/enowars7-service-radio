# This is a configuration file required by the checker.
import multiprocessing

worker_class = "uvicorn.workers.UvicornWorker"
workers = min(4, 1)
bind = "0.0.0.0:9060"
timeout = 90
keepalive = 3600
preload_app = True
