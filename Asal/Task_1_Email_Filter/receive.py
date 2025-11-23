import pika
import time

def main():
    # 1. Connect to your RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 2. Make sure the 'hello' queue exists
    channel.queue_declare(queue='hello')

    # 3. Define the "callback" function
    # This function will be called by Pika every time it receives a message.
    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}") # Decode the message from bytes
        # Simulate a 5-second task
        print(" [ ] Working for 5 seconds...")
        time.sleep(5)
        print(" [✓] Done")

    # 4. Tell Pika to use your callback function for the 'hello' queue
    channel.basic_consume(
        queue='hello',
        on_message_callback=callback,
        auto_ack=True  # Automatically acknowledge the message (we'll change this later)
    )

    # 5. Start listening for messages (this loop runs forever)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')