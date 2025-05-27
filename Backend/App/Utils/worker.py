import pycamunda.externaltask
import time
import requests
import base64
import json

ENGINE_URL = 'http://localhost:8080/engine-rest'
WORKER_ID = 'python-worker'


def fetch_and_handle():
    fetch = pycamunda.externaltask.FetchAndLock(
        url=ENGINE_URL,
        worker_id=WORKER_ID,
        max_tasks=1
    )
    fetch.add_topic(name='ApiTransfer', lock_duration=10000)
    tasks = fetch()

    for task in tasks:
        api_response = task.variables.get('apiTransfer').value

        print(f"Odebrana odpowiedź API: {api_response}")

        complete = pycamunda.externaltask.Complete(
            url=ENGINE_URL,
            id_=task.id_,
            worker_id=WORKER_ID
        )
        complete()


# Główna pętla


if __name__ == '__main__':
    while True:
        try:
            fetch_and_handle()
        except requests.exceptions.RequestException as e:
            print(f"Błąd połączenia z Camundą: {e}")
        time.sleep(2)