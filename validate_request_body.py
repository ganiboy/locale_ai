from flask_api import status
from datetime import datetime
from global_exception_handler import *


def validate_params(param, data_type, error_msg):
    if not type(param) == data_type:
        if param is not None:
            raise ValidationError(error_msg, status.HTTP_400_BAD_REQUEST)


def validate_keys(data, key, datatype):
    try:
        validate_params(data[key], datatype, "%s data type mismatch, %s expected to be %s" % (key, key, datatype))
    except KeyError:
        raise ValidationError("%s is missing in request body" % key, status.HTTP_400_BAD_REQUEST)


def validate_date(data, key):
    try:
        validate_params(data[key], str, "%s data type mismatch, %s expected to be date string" % (key, key))
        if data[key]:
            if data[key] != datetime.strptime(data[key], "%m/%d/%Y %H:%M:%S").strftime("%-m/%-d/%Y %-H:%M:%S"):
                raise ValidationError("%s format mismatch, please send month/date/year hour:minute:seconds " % key,
                                      status.HTTP_400_BAD_REQUEST)
    except KeyError:
        raise ValidationError("%s is missing in request body" % key, status.HTTP_400_BAD_REQUEST)
    except ValueError:
        raise ValidationError("%s format mismatch, please send month/date/year hour:minute:seconds " % key,
                              status.HTTP_400_BAD_REQUEST)
