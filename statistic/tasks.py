from Miners.celery import app
from .service import add_stats_to_db


@app.task
def add_new_stats():
    add_stats_to_db()
