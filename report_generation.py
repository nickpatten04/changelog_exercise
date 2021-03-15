from contants import VALIDATION_LIST, DATAFRAME
from dataframe_cleaner import DataframeCleaner
from test_utilities import prepare_validation

rules = prepare_validation(VALIDATION_LIST)


def print_bad_rows():
    dc = DataframeCleaner(DATAFRAME)
    dc.validate_columns(rules=rules, inplace=True)
    dc.cancel_bad_acounts(inplace=True)
    for index, row in dc.df[dc.df["applied_rules"].notna()].iterrows():
        print(row)


def print_good_rows():
    dc = DataframeCleaner(DATAFRAME)
    dc.validate_columns(rules=rules, inplace=True)
    dc.cancel_bad_acounts(inplace=True)
    for index, row in dc.df[dc.df["applied_rules"].isna()].iterrows():
        print(row)


def print_all_rows():
    dc = DataframeCleaner(DATAFRAME)
    dc.validate_columns(rules=rules, inplace=True)
    dc.cancel_bad_acounts(inplace=True)
    for index, row in dc.df.iterrows():
        print(row)


if __name__ == "__main__":
    print_bad_rows()