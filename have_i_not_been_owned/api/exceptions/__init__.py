from connexion import ProblemException


class HaveIBeenOwnedApiException(ProblemException):
    pass


class DomainNotFound(HaveIBeenOwnedApiException):
    def __init__(self, domain: str):
        super().__init__(
            status=404,
            type=self.__class__.__name__,
            title="Domain not found",
            detail=f"The domain {domain!r} is not present in any data breaches.",
            ext={
                "domain": domain
            }
        )

        self.domain = domain


class EmailNotFound(HaveIBeenOwnedApiException):
    def __init__(self, email: str):
        super().__init__(
            status=404,
            type=self.__class__.__name__,
            title="Email not found",
            detail=f"The email {email!r} is not present in any data breaches.",
            ext={
                "email": email
            }
        )

        self.email = email


class BreachNameAlreadyExists(HaveIBeenOwnedApiException):
    def __init__(self, breach_name: str):
        super().__init__(
            status=409,
            type=self.__class__.__name__,
            title="Breach already exists",
            detail=f"The breach {breach_name!r} already exists.",
            ext={
                "breach_name": breach_name
            }
        )

        self.breach_name = breach_name
