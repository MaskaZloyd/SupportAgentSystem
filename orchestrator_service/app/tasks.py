from celery import Celery
from kafka import KafkaProducer
import json
from . import config

celery_app = Celery(
    'orchestrator_tasks',
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_RESULT_BACKEND
)

#TODO: сделать ленивую загрузку kafka producer
try:
    producer = KafkaProducer(
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print(f"KafkaProducer initialized successfully for tasks: {config.KAFKA_BOOTSTRAP_SERVERS}")
except Exception as e:
    print(f"Failed to initialize KafkaProducer for tasks: {e}")
    producer = None

@celery_app.task
def publish_ticket_event(event_type: str, ticket_data: dict):
    if not producer:
        print("Kafka producer not available. Cannot publish event.")
        #TODO: добавить логику повторной попытки или обработки ошибки
        return

    message = {
        'event_type': event_type,
        'payload': ticket_data
    }
    try:
        producer.send(config.TICKET_EVENTS_TOPIC, value=message)
        producer.flush()
        print(f"Event '{event_type}' for ticket '{ticket_data.get('id')}' published to Kafka topic '{config.TICKET_EVENTS_TOPIC}'.")
    except Exception as e:
        print(f"Error publishing to Kafka: {e}")