class HomeworkException(Exception):
    pass


class SendMessageError(HomeworkException):
    pass


class StatusCodeError(HomeworkException):
    pass


class HomeworkStatusError(HomeworkException):
    pass


class TokensError(HomeworkException):
    pass
