import io
from gtts import gTTS
from flask import send_file
from Backend.App.API.api_connector import api_translate_text
from Backend.App.Models.house_model import get_house_by_user_and_house_id, get_user_house_by_userID_houseID
from Backend.App.Models.user_model import get_user_by_login
from Backend.App.Utils.language_for_gtts import resolve_gtts_language
from Backend.App.Utils.session_helper import get_identity_context, log_and_message_response, Statuses


def generate_greeting(data):
    context = get_identity_context()

    house_id = data.get("HouseID")
    if not house_id:
        return log_and_message_response("HouseID missing", Statuses.BAD_REQUEST)

    if context["is_house_session"]:
        if context["house_id"] != house_id:
            return log_and_message_response("Access denied to this house", Statuses.FORBIDDEN)

    elif context["is_user_session"]:
        try:
            user = get_user_by_login(context["user_login"])
            if not user:
                return log_and_message_response("User not found", Statuses.NOT_FOUND)
            user_id = user.data["UserID"]
        except Exception as e:
            return log_and_message_response("Error with getting user info", Statuses.BAD_REQUEST, "error", e)

        try:
            link = get_user_house_by_userID_houseID(user_id, house_id)
            if not link or not link.data:
                return log_and_message_response("User has no access to this house", Statuses.FORBIDDEN)
        except Exception as e:
            return log_and_message_response("Error verifying access to house", Statuses.BAD_REQUEST, "error", e)

    else:
        return log_and_message_response("Invalid session", Statuses.UNAUTHORIZED)

    try:
        house, status = get_house_by_user_and_house_id(house_id)
        if status != Statuses.OK:
            return house, status
        house_name = house.get("HouseName", "")
        country_code = house.get("CountryCode", "")
    except Exception as e:
        return log_and_message_response("Failed to fetch house data", Statuses.BAD_REQUEST, "error", e)

    if context["is_house_session"]:
        text = f"Welcome in {house_name}"
    elif context["is_user_session"]:
        text = f"Welcome {context['user_login']} in {house_name}"
    else:
        return log_and_message_response("Invalid session", Statuses.UNAUTHORIZED)

    try:
        lang = resolve_gtts_language(country_code)
        translated_text = api_translate_text(text, lang)
        tts = gTTS(text=translated_text, lang=lang)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return send_file(mp3_fp, mimetype="audio/mpeg"), Statuses.OK
    except Exception as e:
        return log_and_message_response("Failed to generate greeting audio", Statuses.BAD_REQUEST, "error", e)
