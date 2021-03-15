import json
from typing import Tuple

import numpy as np
import pandas as pd

from contants import DATAFRAME
from rule import Rule


class DataframeCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_column_fill_rates(self):
        fill_rates = 100 - self.df.isnull().sum() * 100 / len(self.df)
        fill_rate_df = pd.DataFrame({"fill_rate": fill_rates})
        fill_rate_df.index.name = "column_name"
        return fill_rate_df

    @staticmethod
    def _transform_validate_columns_data_list(data_list):
        output = []
        for _dict in data_list:
            indexes = _dict["indexes"]
            for index in indexes:
                searched_dict = next(filter(lambda x: x.get("index") == index, output), None)
                if searched_dict:
                    searched_dict["applied_rules"].append(_dict["applied_rule"])
                    if _dict["column"] in searched_dict["rule_descriptions"].keys():
                        searched_dict["rule_descriptions"][_dict["column"]].append(
                            _dict["rule_description"]
                        )
                    else:
                        searched_dict["rule_descriptions"][_dict["column"]] = [
                            _dict["rule_description"]
                        ]
                else:
                    output.append(
                        {
                            "index": index,
                            "applied_rules": [_dict["applied_rule"]],
                            "rule_descriptions": {_dict["column"]: [_dict["rule_description"]]},
                        }
                    )
        for _dict in output:
            _dict["rule_descriptions"] = json.dumps(_dict["rule_descriptions"])
        return output

    def validate_columns(self, rules: Tuple[Rule], inplace=False):
        validation_df = self.df.copy()
        np.empty((len(validation_df), 0)).tolist()
        validation_df["applied_rules"] = np.empty((len(validation_df), 0)).tolist()
        validation_df["rule_descriptions"] = None
        cast_lambdas = lambda x: "lambda function" if x == "<lambda>" else x
        data_list = []
        for rule in rules:
            data = {}
            indexes = validation_df[validation_df[rule.column].apply(rule.rule)].index
            validation_df.iloc[indexes]["applied_rules"].map(lambda x: x.append(rule.rule.__name__))
            if rule.column in data.keys():
                data[rule.column].append(cast_lambdas(rule.rule.__name__))
            else:
                data[rule.column] = [rule.description or rule.rule.__name__]
            data["indexes"] = tuple(indexes)
            data["column"] = rule.column
            data["applied_rule"] = cast_lambdas(rule.rule.__name__)
            data["rule_description"] = rule.description or cast_lambdas(rule.rule.__name__)
            data_list.append(data)
            for index in indexes:
                validation_df.at[index, "rule_descriptions"] = json.dumps(data)
        validation_to_append = pd.DataFrame(
            self._transform_validate_columns_data_list(data_list)
        ).set_index("index")
        if inplace:
            self.df = self.df.join(validation_to_append)
        else:
            return validation_df.drop(["applied_rules", "rule_descriptions"], axis=1).join(
                validation_to_append
            )

    def cancel_bad_acounts(self, inplace=False):
        df = self.df.copy()
        indexes = df[df["applied_rules"].notna()].index
        for index in indexes:
            if inplace:
                self.df.at[index, "status"] = "cancelled"
            else:
                df.at[index, "status"] = "cancelled"
        return df if not inplace else None


if __name__ == "__main__":
    from test_utilities import validate_dates

    print(DATAFRAME["status"].value_counts())
    rules = (Rule("birth_date", validate_dates, "invalid date"),)
    dc = DataframeCleaner(DATAFRAME)
    dc.validate_columns(rules, inplace=True)
    print(dc.df)
    print(dc.df.shape)
    dc.cancel_bad_acounts(inplace=True)
    print(dc.df[dc.df["applied_rules"].notna()])
    print(dc.df.shape)
    # print(dc.df.iloc[8900])
    # print(DataframeCleaner(DATAFRAME).validate_columns(rules))
    # print(DATAFRAME.query("status == 'active' and id > 200"))
    # print(test)
