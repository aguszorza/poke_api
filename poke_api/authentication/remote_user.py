class RemoteUser:

    def __init__(self, user_data):
        self.id = user_data.get("id")
        self.username = user_data.get("username")
        self.email = user_data.get("email")
        self.types = user_data.get("types", [])

    @property
    def is_authenticated(self):
        return True
