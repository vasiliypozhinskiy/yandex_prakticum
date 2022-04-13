import backoff
import requests
from requests.exceptions import ConnectionError

from settings import TestSettings


@backoff.on_exception(backoff.expo, exception=ConnectionError)
def es_waiting():
    requests.get(f'{TestSettings().es_host}/_cluster/health')


if __name__ == '__main__':
    es_waiting()
