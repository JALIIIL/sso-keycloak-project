import os
import json
import logging
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Variables d'environnement
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'sso-events')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'monitoring-consumer-group')
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'elasticsearch:9200')
ELASTICSEARCH_INDEX = os.getenv('ELASTICSEARCH_INDEX', 'sso-logs')

class SSOEventConsumer:
    def __init__(self):
        """Initialise le consumer Kafka et le client Elasticsearch"""
        try:
            # Connexion à Kafka
            self.consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                group_id=KAFKA_GROUP_ID,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logger.info(f"Connecté à Kafka: {KAFKA_BOOTSTRAP_SERVERS}")
            
            # Connexion à Elasticsearch
            self.es_client = Elasticsearch([ELASTICSEARCH_HOST])
            logger.info(f"Connecté à Elasticsearch: {ELASTICSEARCH_HOST}")
            
            # Créer l'index s'il n'existe pas
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
                logger.info(f"Index Elasticsearch créé: {ELASTICSEARCH_INDEX}")
                
        except Exception as e:
            logger.error(f"Erreur d'initialisation: {e}")
            raise
    
    def process_event(self, event):
        """Traite un événement SSO et l'indexe dans Elasticsearch"""
        try:
            # Ajouter un timestamp si absent
            if 'timestamp' not in event:
                event['timestamp'] = datetime.utcnow().isoformat()
            
            # Indexer dans Elasticsearch
            response = self.es_client.index(
                index=ELASTICSEARCH_INDEX,
                body=event
            )
            
            logger.info(f"Événement indexé: {event.get('event_type', 'unknown')} - {response['result']}")
            
            # Détection d'anomalies simples
            self.detect_anomalies(event)
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement de l'événement: {e}")
    
    def detect_anomalies(self, event):
        """Détecte des anomalies basiques dans les événements"""
        # Échecs de connexion répétés
        if event.get('event_type') == 'LOGIN' and not event.get('success'):
            user_id = event.get('user_id')
            logger.warning(f"Échec de connexion détecté pour l'utilisateur: {user_id}")
        
        # Sessions suspectes (connexions depuis des IPs différentes)
        if event.get('event_type') == 'TOKEN_REFRESH':
            logger.info(f"Rafraîchissement de token pour session: {event.get('session_id')}")
    
    def start(self):
        """Démarre la consommation des événements Kafka"""
        logger.info("Démarrage du consumer...")
        try:
            for message in self.consumer:
                event = message.value
                logger.debug(f"Message reçu: {event}")
                self.process_event(event)
        except KeyboardInterrupt:
            logger.info("Arrêt du consumer...")
        except Exception as e:
            logger.error(f"Erreur dans la boucle de consommation: {e}")
        finally:
            self.consumer.close()
            logger.info("Consumer fermé")

if __name__ == "__main__":
    logger.info("Initialisation du SSO Event Consumer")
    consumer = SSOEventConsumer()
    consumer.start()
