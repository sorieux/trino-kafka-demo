# Trino Kafka Demo: A Step-by-Step Guide

Welcome to the "Trino Kafka Demo" project! 
This guide will walk you through setting up and using this demonstration, showcasing how to query Kafka topics using SQL with Trino. 
We'll cover everything from installation to viewing your Kafka messages.


## Setting the Stage: Understanding the Components

Before diving into the setup, let's get familiar with the key components of our project:

* **Trino:** The powerful SQL query engine we'll use to interrogate data directly from Kafka.
* **Kafka:** Our data streaming platform, handling the flow of social media posts.
* **Zookeeper:** Works behind the scenes to manage Kafka's cluster state and configurations.
* **Redpanda Console:** A web-based UI for visualizing and managing our Kafka data streams.
* **PostgreSQL:** Our relational database, used to demonstrate data storage and retrieval.

### Prerequisites

- Docker and Docker Compose
- Python 3.x

### Project Structure

```
trino-kafka-demo/
├── docker-compose.yml # Docker Compose configuration file to set up and run Kafka, Trino, and PostgreSQL.
├── kafka_producer/
│ ├── init.py
│ └── main.py # The main Python script for the Kafka producer.
├── setup.py # Setup script for the Kafka producer package, useful for installing the package.
└── trino/ # Trino configuration files and SQL scripts.
└── etc/
    ├── catalog/
    │ ├── kafka.properties # Configuration for the Kafka connector in Trino.
    │ └── postgres.properties # Configuration for the PostgreSQL connector in Trino.
    ├── config.properties # General Trino server configuration.
    ├── jvm.config # JVM configuration for Trino.
    └── kafka/
        └── demo.fake_social_media.json # JSON file defining the structure of the Kafka topic for Trino.
```

## Step 1: Installation and Setup

1. **Clone the Repository:**

Open your terminal and clone the project repository.

```bash
git clone https://github.com/sorieux/trino-kafka-demo.git
```

2. **Install Dependencies:**

Ensure Python 3 is installed, then run:

```bash
pip install .
```

This command installs all required Python libraries, including the Kafka client and Faker for data generation.

3. **Launch with Docker Compose:**

Bring our environment to life using Docker:

```bash
docker-compose up -d
```

This starts all the necessary services: Kafka, Zookeeper, Trino, Redpanda Console, and PostgreSQL.


## Step 2: Simulating Social Media Data

Now, let's generate some data for a fictional social network. Our main.py script uses Faker to create these simulated social media posts.

1. **Single Batch:** To send a fixed number of posts to Kafka, run:

```bash
kafka-producer demo.fake_social_media --count 20 
```

2. **Continuous Mode:** Mimic a live stream by sending posts continuously:

```bash
kafka-producer demo.fake_social_media --continuous
```

> [!NOTE] 
> It's crucial to use the topic name demo.fake_social_media as this is the topic for which Trino configuration is set. 
> This can be found in the `trino/etc/kafka/demo.fake_social_media.json` and `trino/etc/catalog/kafka.properties files.


## Step 3: Observing Kafka in Action

With data flowing into Kafka, let's see it in action:

1. **Open Redpanda Console:** Head to `http://localhost:8000` on your browser.
2. **Explore Kafka Topics:** Navigate to the topic you've been publishing to and observe the incoming messages.


## Step 4: Querying with Trino

Time to query our data using Trino:

1. **Access Trino:** Use the Trino CLI or SQL client with the following configuration:

   - **JDBC URL:** `jdbc:trino://localhost:8080`
   - **Username:** `admin`
   - **Password:** No password is required for this demo; leave the field blank.
   - **Driver Name:** `Trino`. The Trino driver can be downloaded from [Trino's Driver Maven Repository](https://repo1.maven.org/maven2/io/trino/trino-jdbc/433/trino-jdbc-433.jar). 
For more details about this driver, refer to the [Trino JDBC Documentation](https://trino.io/docs/current/client/jdbc.html).

For assistance in configuring DBeaver with Trino, consult the [DBeaver Configuration Guide](https://docs.starburst.io/clients/dbeaver.html).
Additionally, if you prefer using the Trino CLI, detailed information is available in the [Trino CLI Documentation](https://trino.io/docs/current/client/cli.html).


2. **Run a Basic Query:** Start with a simple select statement:

```SQL
SELECT
	username,
	post_content,
	likes,
	comments,
	shares,
	timestamp
FROM
	kafka.demo.fake_social_media

```

We can explore the details of your request on Trino UI to `http://localhost:8000` on your browser. 

3. **Data Transfer to PostgreSQL:** Execute a query to transfer data to PostgreSQL:

```SQL
CREATE TABLE postgres.public.social_media AS
SELECT
	username,
	post_content,
	likes,
	comments,
	shares,
	timestamp
FROM
	kafka.demo.fake_social_media
```

4. **Check the data on PostgreSQL table:** Execute this query for example

```SQL
SELECT * FROM postgres.public.social_media
```

## Wrapping Up

Congratulations! 
You've just set up a fully functional demo showcasing the integration of Kafka, Trino, and PostgreSQL. 
Now, you're ready to explore further, perhaps customizing the data streams or queries.

## Useful Resources and Acknowledgments

In the journey of creating this demo, several resources have been invaluable. 
Whether you're looking to deepen your understanding or troubleshoot issues, the following links can be of great assistance:

1. **Trino Documentation**: For comprehensive details on Trino's capabilities and configurations.
   - [Trino Official Documentation](https://trino.io/docs/current/index.html)
   - [Kafka connector tutorial](https://trino.io/docs/current/connector/kafka-tutorial.html)

2. **Kafka and Zookeeper**: To understand more about data streaming and management.
   - [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
   - [Apache Zookeeper Documentation](https://zookeeper.apache.org/doc/current/)

3. **Faker Library for Python**: For generating fake data for your applications.
   - [Faker on PyPI](https://pypi.org/project/Faker/)


## Contributing

Interested in contributing or have suggestions? 
Great! Feel free to contact me for any queries or submit a [Pull Request](https://github.com/sorieux/trino-kafka-demo/pulls) with your improvements. 


## License

This project is open-source under the MIT License.
