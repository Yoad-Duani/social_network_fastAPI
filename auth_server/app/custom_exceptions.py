



class UnverifiedTokenException(Exception):
    def __init__(self, message="Unverified token"):
        self.message = message
        super().__init__(self.message)


class EmailAlreadyVerifiedException(Exception):
    def __init__(self, message="The email address has already been verified"):
        self.message = message
        super().__init__(self.message)