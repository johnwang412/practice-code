#!/usr/bin/env python3
"""
Script to test that the KV store can persist data across service restarts.
Assumes the KV store service is already running on localhost:5001.
"""

import http
import logging
import random
import string
import time

import requests

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

BASE_URL = "http://localhost:5001"


def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def put_key_value(key, value):
    """Store a key-value pair in the store."""
    url = f"{BASE_URL}/put"
    try:
        response = requests.put(url, json={"key": key, "value": value})
        if response.status_code == 200:
            LOGGER.info(f"Successfully stored key '{key}' with value '{value[:20]}...'")
            return True
        else:
            LOGGER.error(f"Failed to store key '{key}': {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        LOGGER.error("Connection failed to KV store service")
        return False


def get_key_value(key):
    """Retrieve a value for the given key."""
    url = f"{BASE_URL}/get?key={key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            value = response.text
            LOGGER.info(f"Successfully retrieved key '{key}': '{value[:20]}...'")
            return value
        elif response.status_code == 404:
            LOGGER.warning(f"Key '{key}' not found")
            return None
        else:
            LOGGER.error(f"Failed to retrieve key '{key}': {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        LOGGER.error("Connection failed to KV store service")
        return None


def restart_service():
    """Restart the KV store service by triggering the harikari endpoint.

    This will cause the worker to crash and a new one to be spawned,
    testing if the data persists across service restarts.
    """
    LOGGER.info("Restarting the KV store service via harikari endpoint...")
    try:
        # Call the harikari endpoint to kill the worker
        try:
            requests.post(f"{BASE_URL}/harikari")
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError):
            # This is expected since the server will crash
            LOGGER.info("Server crashed as expected")

        # Wait for the service to come back up
        max_retries = 30
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(f"{BASE_URL}/health")
                if response.status_code == 200:
                    LOGGER.info("KV store service is up and running again")
                    time.sleep(2)  # Give an extra moment for the service to fully initialize
                    return True
            except requests.exceptions.ConnectionError:
                pass

            LOGGER.info(f"Waiting for service to restart... (attempt {retries+1}/{max_retries})")
            time.sleep(1)
            retries += 1

        LOGGER.error("KV store service failed to restart within the expected time")
        return False
    except Exception as e:
        LOGGER.error(f"Failed to restart service: {e}")
        return False


def test_persistence():
    """Test that data persists across service restarts."""
    LOGGER.info("Starting persistence test...")

    # Generate test data - a mix of small and medium values
    test_data = {
        f"test_key_{i}": generate_random_string(
            random.choice([100, 1000, 5000])
        ) for i in range(10)
    }

    # Add a special marker key to identify this test run
    test_marker = f"test_marker_{int(time.time())}"
    test_data[test_marker] = "PERSISTENCE_TEST_MARKER"

    # Step 1: Store all key-value pairs
    LOGGER.info("Step 1: Storing key-value pairs")
    for key, value in test_data.items():
        success = put_key_value(key, value)
        if not success:
            LOGGER.error("Failed to store data, aborting test")
            return False

    # Step 2: Verify all keys are stored correctly
    LOGGER.info("Step 2: Verifying stored key-value pairs")
    all_keys_present = True
    for key, expected_value in test_data.items():
        actual_value = get_key_value(key)
        if actual_value != expected_value:
            LOGGER.error(f"Value mismatch for key '{key}' before restart")
            all_keys_present = False

    if not all_keys_present:
        LOGGER.error("Not all keys were stored correctly, aborting test")
        return False

    # Step 3: Restart the service
    LOGGER.info("Step 3: Restarting the KV store service")
    if not restart_service():
        LOGGER.error("Failed to restart service, aborting test")
        return False

    # Step 4: Verify all keys are still present after restart
    LOGGER.info("Step 4: Verifying key-value pairs after restart")
    all_keys_preserved = True
    for key, expected_value in test_data.items():
        actual_value = get_key_value(key)
        if actual_value != expected_value:
            LOGGER.error(f"Value mismatch for key '{key}' after restart")
            all_keys_preserved = False

    if all_keys_preserved:
        LOGGER.info("SUCCESS: All keys persisted across service restart")
        return True
    else:
        LOGGER.error("FAILURE: Some keys were lost after service restart")
        return False


def main():
    """Run the persistence test and display results."""
    start_time = time.time()

    success = test_persistence()

    end_time = time.time()
    duration = end_time - start_time

    if success:
        LOGGER.info(f"Persistence test passed in {duration:.2f} seconds")
    else:
        LOGGER.error(f"Persistence test failed after {duration:.2f} seconds")

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())