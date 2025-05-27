import pycamunda.externaltask
import time
import requests
from Backend.App.Utils.camunda_task_handler import get_api_data, handle_default
from Backend.App.Utils.session_helper import log_and_message_response, Statuses

ENGINE_URL = 'http://localhost:8080/engine-rest'
WORKER_ID = 'python-worker'
LOCK_DURATION = 10000
POLL_TIMEOUT_MS = 5000
TOPICS = [
    'ApiTransfer',
]
TOPIC_HANDLERS = {
    'ApiTransfer': get_api_data,
}

def manage_tasks():
    api_result = None
    try:
        fetch = pycamunda.externaltask.FetchAndLock(
            url=ENGINE_URL,
            worker_id=WORKER_ID,
            max_tasks=TOPICS.__len__(),
            async_response_timeout=POLL_TIMEOUT_MS
        )

        for topic in TOPIC_HANDLERS.keys():
            fetch.add_topic(name=topic, lock_duration=LOCK_DURATION)

        tasks = fetch()

        if not tasks:
            return log_and_message_response("No tasks found", Statuses.NOT_FOUND, "error")

        for task in tasks:
            handler = TOPIC_HANDLERS.get(task.topic_name, handle_default)

            try:
                result = handler(task)

                complete = pycamunda.externaltask.Complete(
                    url=ENGINE_URL,
                    id_=task.id_,
                    worker_id=WORKER_ID
                )
                complete()

                if task.topic_name == "ApiTransfer":
                    api_result = result

                print(f"Completed task: {task.id_} (topic: {task.topic_name})")
            except Exception as e:
                fail = pycamunda.externaltask.HandleFailure(
                    url=ENGINE_URL,
                    id_=task.id_,
                    worker_id=WORKER_ID,
                    error_message=str(e),
                    error_details=str(e),
                    retries=0,
                    retry_timeout=1000
                )
                fail()
                return log_and_message_response("Error handling task {task.id_}", Statuses.BAD_REQUEST, "error", e)

        return api_result.json(), Statuses.OK
    except Exception as e:
        return log_and_message_response("Failed to manage Camunda", Statuses.BAD_REQUEST, "error", e)