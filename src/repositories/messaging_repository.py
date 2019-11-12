from firebase_admin.messaging import Message, send


# This registration token comes from the client FCM SDKs.
def send_message_to_device(message, registration_token):
    if registration_token == "":
        return False

    fcm_message = Message(
        data=message,
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    send(fcm_message)
    return True
