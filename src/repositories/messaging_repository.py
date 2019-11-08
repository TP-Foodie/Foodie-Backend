from firebase_admin import messaging
import logger


# This registration token comes from the client FCM SDKs.
def send_message_to_device(message, registration_token):
    if registration_token == "":
        return

    fcm_message = messaging.Message(
        data=message,
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(fcm_message)
    logger.info("MESSAGE SENT: " + response)
