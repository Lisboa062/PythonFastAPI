class OrderNotFoundException(Exception):
    pass


class NotAuthorizedException(Exception):
    pass


class ItemNotFoundException(Exception):
    pass


class EmailUsedException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass