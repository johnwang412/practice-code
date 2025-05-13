import http
import logging

import requests
import time

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)


def generate_large_string(size_in_bytes):
    """Generate a random string of specified size in bytes."""
    return 'a' * size_in_bytes


def send_puts(url, key_idx_start, num_requests, value_length, repeat) -> int:
    """
    :param repeat: Number of times to repeat the requests with same keys
    
    :return: Number of successful PUT requests (HTTP 200)
    """
    kv_store_size = 0
    num_200s = 0
    for _ in range(repeat):
        i = key_idx_start
        for i in range(key_idx_start, key_idx_start + num_requests):
            key = f"key_{i}"
            value = generate_large_string(value_length)
            response = None
            try:
                response = requests.put(url, json={"key": key, "value": value})
            except (http.client.RemoteDisconnected, requests.exceptions.ConnectionError):
                LOGGER.error(f"Connection closed by server while storing {key}. KV store: {kv_store_size}.")
                break
            
            if response and response.status_code == 200:
                ret_json = response.json()
                kv_store_size = ret_json.get('kv_store_size', 0)
                num_200s += 1
            else:
                LOGGER.error(f"Failed to store {key}: {response.status_code}. KV store: {kv_store_size}.")
                break
            LOGGER.info(f'i: {i}, kv_store_size: {kv_store_size}')
    
    return num_200s

"""
PERF:
    - mem_limit: 64m
    - memswap_limit: 64m

"""

def main():
    base_url = "http://localhost:5001"
    endpoint = "/put"
    # Num pairs of 128x128 char values that fit in memory of docker container
    #   booted with docker-compose with mem_limit: 32m and memswap_limit: 32m
    num_pairs_within_memory = 5
    num_pairs = 500  # Number of MB values to store
    value_size = 1028 * 1028

    start_time = time.time()
    num_200s = send_puts(
        url=f'{base_url}{endpoint}', 
        key_idx_start=0, 
        num_requests=num_pairs_within_memory, 
        value_length=value_size,
        repeat=1,
    )
    end_time = time.time()
    LOGGER.info(f'RPS within memory: {num_200s / (end_time - start_time):.2f} requests/sec')
    

if __name__ == "__main__":
    main()
