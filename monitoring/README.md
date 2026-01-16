# 📊 Monitoring - Kafka Consumer

This directory contains the Python Kafka consumer that monitors SSO events from Keycloak and indexes them into Elasticsearch for analysis and visualization in Kibana.

## 🎯 Purpose

The monitoring consumer:
- Consumes events from Kafka topics (login attempts, token refreshes, etc.)
- Performs basic anomaly detection (failed logins, suspicious patterns)
- Indexes events into Elasticsearch for long-term storage
- Enables real-time monitoring through Kibana dashboards

## 📋 Prerequisites

- Python 3.9+
- Kafka broker running
- Elasticsearch cluster running
- Docker & Docker Compose (for containerized deployment)

## 📁 Structure

```
monitoring/
├── consumer.py         # Main Kafka consumer script
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker image for consumer
└── README.md          # This file
```

## 🚀 Installation

### Local Development

1. Install dependencies:

```bash
cd monitoring
pip install -r requirements.txt
```

2. Configure environment variables (see `.env.example` in project root):

```bash
export KAFKA_BOOTSTRAP_SERVERS=localhost:9092
export KAFKA_TOPIC=keycloak-events
export KAFKA_GROUP_ID=sso-monitoring
export ELASTICSEARCH_HOST=http://localhost:9200
export ELASTICSEARCH_INDEX=sso-logs
```

3. Run the consumer:

```bash
python consumer.py
```

### Docker Deployment

The consumer is automatically deployed with the full stack:

```bash
docker-compose -f docker-compose.dev.yml up -d
```

## 📊 Environment Variables

| Variable | Description | Default |
|----------|-------------|----------|
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker address | `kafka:9092` |
| `KAFKA_TOPIC` | Kafka topic to consume | `keycloak-events` |
| `KAFKA_GROUP_ID` | Consumer group ID | `sso-monitoring` |
| `ELASTICSEARCH_HOST` | Elasticsearch URL | `http://elasticsearch:9200` |
| `ELASTICSEARCH_INDEX` | Index name for events | `sso-logs` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🔍 Event Types Monitored

- **LOGIN** - User login attempts (success/failure)
- **LOGOUT** - User logout events
- **TOKEN_REFRESH** - Token refresh operations
- **CODE_TO_TOKEN** - Authorization code exchange
- **CLIENT_LOGIN** - Client authentication events

## 🛡️ Anomaly Detection

The consumer performs basic anomaly detection:

- **Repeated login failures**: Tracks failed login attempts per user
- **Suspicious token activity**: Monitors unusual token refresh patterns
- **Brute force detection**: Identifies multiple failed attempts

Anomalies are logged with WARNING level and can trigger alerts in Kibana.

## 📈 Elasticsearch Index Mapping

Events are indexed with the following structure:

```json
{
  "timestamp": "2026-01-16T14:00:00Z",
  "event_type": "LOGIN",
  "user_id": "user123",
  "session_id": "abc-123",
  "client_id": "dummy-app",
  "ip_address": "192.168.1.1",
  "success": true,
  "error_message": null
}
```

## 🧪 Testing

### Check consumer logs:

```bash
docker-compose -f docker-compose.dev.yml logs -f kafka-consumer
```

### Verify Elasticsearch indexing:

```bash
curl http://localhost:9200/sso-logs/_search?pretty
```

### Test with sample event:

```bash
# Send a test message to Kafka
docker exec -it sso-kafka kafka-console-producer \
  --broker-list localhost:9092 \
  --topic keycloak-events

# Then paste a JSON event:
{"event_type":"LOGIN","user_id":"testuser","success":true}
```

## 🐛 Debugging

### Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python consumer.py
```

### Common issues:

**Kafka connection refused**
- Verify Kafka is running: `docker-compose ps kafka`
- Check Kafka logs: `docker-compose logs kafka`

**Elasticsearch indexing errors**
- Verify Elasticsearch is healthy: `curl http://localhost:9200/_cluster/health`
- Check index exists: `curl http://localhost:9200/_cat/indices?v`

**No events consumed**
- Verify Keycloak event listener is configured
- Check Kafka topic exists: `docker exec sso-kafka kafka-topics --list --bootstrap-server localhost:9092`

## 🔗 Integration with Keycloak

To send Keycloak events to Kafka, configure an Event Listener in Keycloak:

1. Admin Console → Realm Settings → Events
2. Event Listeners → Add `kafka`
3. Configure Kafka connection in Keycloak

## 📊 Kibana Dashboards

Access Kibana at `http://localhost:5601` to create dashboards:

- Login success/failure rates
- Geographic distribution of logins
- Token expiration monitoring
- Security alerts and anomalies

## 🛠️ Technologies

- **kafka-python** - Kafka client library
- **elasticsearch** - Elasticsearch client
- **Python 3.9+** - Runtime environment

## 📝 License

MIT
