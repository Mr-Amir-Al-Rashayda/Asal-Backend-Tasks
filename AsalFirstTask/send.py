import pika

# 1. Connect to your RabbitMQ server
# 'localhost' works because your Docker container is running on your machine.
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Create a "queue" (a mailbox)
# This makes sure the 'hello' queue exists. If it does, nothing happens.
channel.queue_declare(queue='hello')

# 3. Publish the message
channel.basic_publish(
    exchange='',           # The default exchange
    routing_key='hello',   # The name of the queue to send to
    body='Hello World!'    # The message itself
)

print(" [x] Sent 'Hello World!'")

# 4. Close the connection
connection.close()