def get_api_data(task):
    api_response = task.variables.get('apiTransfer').value
    print(f"{api_response}")
    return api_response

def handle_default(task):
    print(f"[{task.topic_name}] No custom handler.")
    return None

def mist_light_off(task):
    print("Mist light off")
    return None

def mist_light_on(task):
    print("Mist light on")
    return None

def open_window(task):
    print("Open window")
    return None

def close_window(task):
    print("Close window")
    return None

def close_solar_panel(task):
    print("Close solar panel")
    return None

def open_solar_panel(task):
    print("Open solar panel")
    return None