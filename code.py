from google.cloud import bigquery
from google.cloud import pubsub_v1
from datetime import datetime, timedelta

PROJECT_ID = 'your-project-id'
DATASET_ID = 'your-dataset-id'
TABLE_ID = 'your-table-id'
TOPIC_NAME = 'your-topic-name'

def check_bq_table(event, context):
    bq_client = bigquery.Client()
    pubsub_client = pubsub_v1.PublisherClient()

    table = bq_client.get_table(f'{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}')

    latest_insert_time = table.created.strftime('%Y-%m-%d %H:%M:%S')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    time_diff = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(latest_insert_time, '%Y-%m-%d %H:%M:%S')

    if time_diff > timedelta(minutes=5):
        message = 'No data inserted in the last 5 minutes'
        topic_path = pubsub_client.topic_path(PROJECT_ID, TOPIC_NAME)
        pubsub_client.publish(topic_path, message.encode())
