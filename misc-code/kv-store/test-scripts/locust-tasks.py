"""
Using this script to do load and throughput testing.
"""
import random
import string

import locust

MAX_KEYS = 100


class KVStoreUser(locust.HttpUser):

    stored_keys = []

    @locust.task
    def put_random_key_value(self):
        """Store a random key-value pair in the KV store."""
        key = "".join(random.choices(string.ascii_lowercase, k=4))
        value = "".join(random.choices(string.ascii_letters + string.digits, k=32))

        resp = self.client.put("/put", json={"key": key, "value": value})
        if resp.status_code == 200:
            if len(self.stored_keys) >= MAX_KEYS:
                self.stored_keys.pop(0)
            self.stored_keys.insert(random.randint(0, 100), key)

    @locust.task(5)
    def get_key(self):
        if not self.stored_keys:
            return
        i = random.randint(0, len(self.stored_keys)-1)
        key = self.stored_keys[i]
        resp = self.client.get(f"/get?key={key}")