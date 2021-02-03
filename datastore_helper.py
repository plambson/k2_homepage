from google.cloud import datastore
import os



def store(entity_dict, kind):
    datastore_client = datastore.Client()
    entity = datastore.Entity(key=datastore_client.key(kind))
    entity.update(entity_dict)
    datastore_client.put(entity)
    return entity.key


def fetch_meetings():
    datastore_client = datastore.Client()
    query = datastore_client.query(kind='meetings')
    meetings = list(query.fetch())
    return meetings


def fetch_messages(key):
    datastore_client = datastore.Client()
    query = datastore_client.query(kind=os.environ["datastore_comms"] )
    entity_key = datastore.Key.from_legacy_urlsafe(key)
    query.add_filter('fk', '=', entity_key)
    query.order = ['-timestr']
    messages = list(query.fetch())
    return messages

def delete_key(key):
    datastore_client = datastore.Client()
    entity_key = datastore.Key.from_legacy_urlsafe(key)
    datastore_client.delete(entity_key)
    return 'deleted'

