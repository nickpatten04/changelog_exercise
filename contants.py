import pandas as pd

import test_utilities as tu
from rule import Rule

DATAFRAME = pd.read_json("dataset.json", lines=True)

DATETIME_VALIDATION = [
    Rule(column=column, rule=tu.validate_dates, description="invalid date")
    for column in ("created_at", "updated_at", "birth_date")
]

AGE_VALIDATION = Rule(column="birth_date", rule=tu.validate_ages, description="invalid age")

EMAIL_VALIDATION = Rule(column="email", rule=tu.validate_emails, description="invalid email")

ZIPCODE_VALIDATION = Rule(column="zip5", rule=tu.validate_zip_codes, description="invalid zip code")

PHONE_VALIDATION = Rule(
    column="phone", rule=tu.validate_phone_numbers, description="invalid phone number"
)

VALIDATION_LIST = [
    DATETIME_VALIDATION,
    AGE_VALIDATION,
    EMAIL_VALIDATION,
    ZIPCODE_VALIDATION,
    PHONE_VALIDATION,
]
