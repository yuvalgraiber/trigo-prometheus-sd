import requests
import json
import time
import os
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TARGET_FILE = '/etc/prometheus/targets.json'

def update_prometheus_targets():
    try:
        response = requests.get('http://inventory_server:1337/inventory', timeout=5)
        response.raise_for_status()
        sensors = response.json()
        
        data = [{"targets": [f"{s}:80" for s in sensors]}]
        
        # Atomic write: write to a temp file and rename (avoids partial reads by Prometheus)
        with open(TARGET_FILE + '.tmp', 'w') as f:
            json.dump(data, f)
        os.replace(TARGET_FILE + '.tmp', TARGET_FILE)
            
        logger.info(f"Successfully updated {len(sensors)} targets.")
    except Exception as e:
        logger.error(f"Failed to update targets: {e}")

if __name__ == "__main__":
    while True:
        update_prometheus_targets()
        time.sleep(30)