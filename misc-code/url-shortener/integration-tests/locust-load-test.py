"""
Using this script to do load and throughput testing.
"""
import random
import string

import locust


class KVStoreUser(locust.FastHttpUser):
    stored_keys = []

    @locust.task
    def put_new_url(self):
        domain = "".join(random.choices(string.ascii_lowercase, k=12))
        path = "".join(random.choices(string.ascii_letters + string.digits, k=12))

        self.client.put('/shorten', json={'url': f'https://{domain}.com/{path}'})
