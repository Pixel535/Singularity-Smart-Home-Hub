def get_api_data(task):
    api_response = task.variables.get('apiTransfer').value
    print(f"{api_response}")
    return api_response

def handle_default(task):
    print(f"[{task.topic_name}] No custom handler.")
    return None