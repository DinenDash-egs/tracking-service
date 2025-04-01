# tracking-service

## Run the queue and producer:
```sh
docker compose up --build  # Build and start if running for the first time
```

RabbitMQ runs on port 15672 (management UI).

The API runs on port 8000.

## If there's service errors:
Run the following commands
```
docker compose down
docker network ls
docker network inspect geolocation-service_default
docker compose up --build
```

## Verify RabbitMQ is running:
To check if RabbitMQ is active and reachable, open:

```
http://localhost:15672
```
Login credentials: guest / guest


## Logs:
```
docker logs geolocation-service
docker logs rabbitmq
```