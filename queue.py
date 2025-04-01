import pika
import os
import time

# Get RabbitMQ hostname and port from environment variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")  # Connect to RabbitMQ inside Docker
RABBITMQ_PORT = 5672  # Internal port

QUEUE_NAME = "geolocation"

# Retry connection logic
while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        )
        break  # Connection successful
    except pika.exceptions.AMQPConnectionError:
        print("Waiting for RabbitMQ to start...")
        time.sleep(5)  # Wait before retrying

channel = connection.channel()

# Declare queue (durable to persist messages)
channel.queue_declare(queue=QUEUE_NAME, durable=True)

def callback(ch, method, properties, body):
    """Process messages received from RabbitMQ queue."""
    print(f"Received message: {body.decode()}")

# Start consuming messages
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

print("Waiting for messages...")
channel.start_consuming()
