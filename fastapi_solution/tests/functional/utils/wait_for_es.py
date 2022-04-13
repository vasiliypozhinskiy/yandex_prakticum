import time
import logging
import requests
from requests.exceptions import ConnectionError

from settings import TestSettings


if __name__ == "__main__":
    while True:
        try:
            res = requests.get(f"{TestSettings().es_host}/_cluster/health")
            if res.status_code == 200:
                break
        except ConnectionError:
            pass

        logging.warning("Wait for elastic. Sleep 1 second.")
        time.sleep(1)
