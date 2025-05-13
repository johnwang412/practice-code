import logging

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)


class KVStore:
    
    def __init__(self):
        self.store = {}

    def put(self, key, value):
        """Store the value with the given key."""
        self.store[key] = value

    def get(self, key):
        """Retrieve the value for the given key."""
        return self.store.get(key, None)