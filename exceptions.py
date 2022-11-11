class HomeworkException(Exception):
    pass
class StatusCodeError(HomeworkException):
    pass
class ResponseError(HomeworkException):
    pass
class StatusKeyError(HomeworkException):
    pass