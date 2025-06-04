import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis_db:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis_db:6379/0')

TICKET_EVENTS_TOPIC = 'ticket_events'