import os
import json
import logging
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from datetime import datetime

"""SSO event consumer: reads events from Kafka and indexes to Elasticsearch.

Environment variables:
 - KAFKA_BOOTSTRAP_SERVERS (default: kafka:9092)
 - KAFKA_TOPIC (default: sso-events)
 - KAFKA_GROUP_ID (default: monitoring-consumer-group)
 - ELASTICSEARCH_HOST (default: http://elasticsearch:9200)
 - ELASTICSEARCH_INDEX (default: sso-logs)
"""

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'sso-events')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'monitoring-consumer-group')
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'http://elasticsearch:9200')
ELASTICSEARCH_INDEX = os.getenv('ELASTICSEARCH_INDEX', 'sso-logs')

class SSOEventConsumer:
    def __init__(self):
        """Initialise le consumer Kafka et le client Elasticsearch"""
        try:
            # Connect to Kafka
            self.consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                group_id=KAFKA_GROUP_ID,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logger.info(f"Connected to Kafka: {KAFKA_BOOTSTRAP_SERVERS}")

            # Connect to Elasticsearch
            self.es_client = Elasticsearch([ELASTICSEARCH_HOST])
            logger.info(f"Connected to Elasticsearch: {ELASTICSEARCH_HOST}")

            # Create index if it doesn't exist
            if not self.es_client.indices.exists(index=ELASTICSEARCH_INDEX):
                self.es_client.indices.create(
                    index=ELASTICSEARCH_INDEX,
                    body={
                        "mappings": {
                            "properties": {
                                "timestamp": {"type": "date"},
                                "event_type": {"type": "keyword"},
                                "user_id": {"type": "keyword"},
                                "session_id": {"type": "keyword"},
                                "client_id": {"type": "keyword"},
                                "ip_address": {"type": "ip"},
                                "success": {"type": "boolean"},
                                "error_message": {"type": "text"}
                            }
                        }
                    }
                )
                logger.info(f"Elasticsearch index created: {ELASTICSEARCH_INDEX}")

        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise
    
    def process_event(self, event):
        """Traite un événement SSO et l'indexe dans Elasticsearch"""
        try:
            # Add timestamp if missing
            if 'timestamp' not in event:
                event['timestamp'] = datetime.utcnow().isoformat()

            # Index into Elasticsearch
            response = self.es_client.index(
                index=ELASTICSEARCH_INDEX,
                body=event
            )

            logger.info(f"Event indexed: {event.get('event_type', 'unknown')} - {response.get('result')}")

            # Simple anomaly detection
            self.detect_anomalies(event)
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement de l'événement: {e}")
    
    def detect_anomalies(self, event):
        """Detects basic anomalies in events"""
        # Repeated login failures
        if event.get('event_type') == 'LOGIN' and not event.get('success'):
            user_id = event.get('user_id')
            logger.warning(f"Login failure detected for user: {user_id}")

        # Suspicious session activity (e.g. token refreshes)
        if event.get('event_type') == 'TOKEN_REFRESH':
            logger.info(f"Token refresh for session: {event.get('session_id')}")
    
    def start(self):
        """Démarre la consommation des événements Kafka"""
        logger.info("Starting consumer...")
        try:
            for message in self.consumer:
                event = message.value
                logger.debug(f"Message reçu: {event}")
                self.process_event(event)
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
        except Exception as e:
            logger.error(f"Error in consumption loop: {e}")
        finally:
            self.consumer.close()
            logger.info("Consumer closed")

if __name__ == "__main__":
    logger.info("Initializing SSO Event Consumer")
    consumer = SSOEventConsumer()
    consumer.start()
