# pylint: disable-msg=too-many-instance-attributes
class UserProfile():

    # pylint: disable-msg=too-many-arguments
    def __init__(
            self, name, last_name, email, profile_image,
            type_of_user, subscription, reputation, messages_sent
    ):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.profile_image = profile_image
        self.type = type_of_user
        self.subscription = subscription
        self.reputation = reputation
        self.messages_sent = messages_sent
