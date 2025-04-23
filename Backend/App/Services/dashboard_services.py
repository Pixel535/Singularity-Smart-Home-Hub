import logging
from Backend.App.Models.dashboard_model import (get_houses_by_user_login, insert_user_house, delete_user_house, update_user_house)
from Backend.App.Utils.session_helper import Statuses

logger = logging.getLogger(__name__)


def get_user_houses():
    houses = get_houses_by_user_login()
    return {"houses": houses}, Statuses.OK


def add_house(house_data):
    return insert_user_house(house_data)


def remove_house(house_data):
    return delete_user_house(house_data)


def edit_house(house_data):
    return update_user_house(house_data)
