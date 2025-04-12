from Backend.App.Models.User.user_model import get_user_by_login
from Backend.App.Models.Dashboard.dashboard_model import get_houses_by_user_login, insert_user_house, delete_user_house, update_user_house

def get_user_houses(user_login):
    user = get_user_by_login(user_login)
    if not user.data:
        return {"msg": "User not found"}, 404

    houses = get_houses_by_user_login(user_login)
    return {"houses": houses}, 200

def add_house(user_login, house_data):
    success = insert_user_house(user_login, house_data)
    if not success:
        return {"msg": "Error adding house"}, 400
    return {"msg": "House added successfully"}, 201

def remove_house(user_login, house_data):
    success = delete_user_house(user_login, house_data)
    if not success:
        return {"msg": "Error removing house"}, 400
    return {"msg": "House removed successfully"}, 200

def edit_house(user_login, house_data):
    success = update_user_house(user_login, house_data)
    if not success:
        return {"msg": "Error updating house"}, 400
    return {"msg": "House updated successfully"}, 200

