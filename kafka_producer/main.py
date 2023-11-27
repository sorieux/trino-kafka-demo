import typer
import json
import random
import time
from faker import Faker
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic

# Initialize Typer app
app = typer.Typer()

# Initialize Faker for data generation
fake = Faker()

# Kafka Configuration
BOOTSTRAP_SERVERS = 'localhost:9093'

# Kafka Producer Configuration
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def create_topic_if_not_exists(topic_name, num_partitions=1, replication_factor=1):
    """
    Ensures that a Kafka topic exists, creating it if necessary.

    Args:
        topic_name (str): Name of the Kafka topic.
        num_partitions (int): Number of partitions for the topic. Default is 1.
        replication_factor (int): Replication factor for the topic. Default is 1.
    """
    admin_client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
    existing_topics = admin_client.list_topics()

    if topic_name not in existing_topics:
        print(f"Creating topic '{topic_name}'.")
        topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
        admin_client.create_topics(new_topics=[topic])

def on_send_success(record_metadata):
    """
    Callback function to execute on successful message delivery.

    Args:
        record_metadata: Metadata for the record that was sent.
    """
    print(f"Message sent to {record_metadata.topic} partition {record_metadata.partition}")

def on_send_error(excp):
    """
    Callback function to execute on message delivery failure.

    Args:
        excp: Exception encountered during message sending.
    """
    print(f"Error encountered: {excp}")

def generate_social_media_post():
    """
    Generates a fictitious social media post using Faker.

    Returns:
        dict: A dictionary representing a social media post.
    """
    # Truncating the timestamp to 23 characters to convert Faker's microsecond precision
    # to millisecond precision (timestamp(3)) for Trino compatibility.
    # Future improvement: refine this for better precision handling.
    timestamp = fake.date_time_this_year().isoformat()[:23]

    return {
        "username": fake.user_name(),
        "post_content": fake.text(),
        "likes": random.randint(0, 1000),
        "comments": random.randint(0, 100),
        "shares": random.randint(0, 500),
        "timestamp": timestamp
    }

def send_post(topic, post):
    """
    Sends a single social media post to the Kafka topic.

    Args:
        topic (str): The Kafka topic to which the post will be sent.
        post (dict): The social media post to be sent.
    """
    future = producer.send(topic, post)
    future.add_callback(on_send_success)
    future.add_errback(on_send_error)

@app.command()
def send_social_media_posts(topic: str, count: int = 10, continuous: bool = False):
    """
    Sends social media posts to a Kafka topic.

    Args:
        topic (str): The Kafka topic to which the posts will be sent.
        count (int): The number of posts to send. Default is 10. Ignored if continuous is True.
        continuous (bool): Whether to send posts continuously. Default is False.
    """
    create_topic_if_not_exists(topic)

    if continuous:
        try:
            while True:
                post = generate_social_media_post()
                send_post(topic, post)
                # Random delay between 1 second and 2 minutes to simulate streaming data
                time.sleep(random.uniform(1, 30))
        except KeyboardInterrupt:
            print("Stopping continuous message sending.")
    else:
        for _ in range(count):
            post = generate_social_media_post()
            send_post(topic, post)

    producer.flush()

if __name__ == "__main__":
    app()
