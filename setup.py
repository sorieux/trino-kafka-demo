from setuptools import setup, find_packages

setup(
    name='kafka-producer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'kafka-python==2.0.2',
        'Faker==20.1.0',
        'typer==0.9.0',
    ],
    entry_points={
        'console_scripts': [
            'kafka-producer=kafka_producer.main:app',
        ],
    },
)