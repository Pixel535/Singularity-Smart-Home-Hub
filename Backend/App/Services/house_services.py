from Backend.App.Models.house_model import get_house_by_user_and_house_id


def get_house_data(user_login, house_id):
    return get_house_by_user_and_house_id(user_login, house_id)