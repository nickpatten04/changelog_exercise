import re
from datetime import datetime

import pandas as pd


def validate_ages(value):
    if not validate_dates(value):
        datetime_value = pd.to_datetime(value, infer_datetime_format=True)
        age = (
            datetime.now().year
            - datetime_value.year
            - (
                (datetime.now().month, datetime.now().day)
                < (datetime_value.month, datetime_value.day)
            )
        )
        return False if age >= 18 else True
    else:
        return True


def validate_dates(value):
    try:
        pd.to_datetime(value, infer_datetime_format=True)
        return False
    except Exception as e:
        return True


def validate_emails(value):
    return False if re.match(r"^.+@.+\.(com|net|org|gov)", str(value).lower()) else True


def validate_zip_codes(value):
    return False if len(str(value)) == 5 else True


def validate_phone_numbers(value):
    return (
        False
        if len(str(value)) == 10
        or (
            len(str(value)) == 11
            and str(value).startswith("1")
            or (len(str(value)) == 12 and str(value).startswith("+1"))
        )
        else True
    )


def prepare_validation(validation_list):
    validation_list_final = []
    for validation in validation_list:
        if type(validation) == list:
            validation_list_final.extend(validation)
        else:
            validation_list_final.append(validation)
    return validation_list_final
