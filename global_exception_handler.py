class ValidationError(Exception):
    def __init__(self, msg, status_code):
        self.msg = msg
        self.status_code = status_code


class FunctionalError(Exception):
    def __init__(self, function_name, msg):
        self.function_name = function_name
        self.msg = msg
