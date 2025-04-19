import logging
from Backend.App.Models.dashboard_model import get_houses_by_user_login, insert_user_house, delete_user_house, update_user_house
from Backend.App.config import Statuses, log_and_message_response

logger = logging.getLogger(__name__)

def get_user_houses(user_login):
    houses = get_houses_by_user_login(user_login)
    log_and_message_response("Getting houses", Statuses.OK, "success", None)
    return {"houses": houses}, Statuses.OK

def add_house(user_login, house_data):
    return insert_user_house(user_login, house_data)

def remove_house(user_login, house_data):
    return delete_user_house(user_login, house_data)


def edit_house(user_login, house_data):
    return update_user_house(user_login, house_data)

