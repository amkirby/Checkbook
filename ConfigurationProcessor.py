import locale
from typing import Any, Dict, List

import yaml


class ConfigurationProcessor():
    
    _instance = None
    
    # def __init__(self) -> None:
    #     self.config_file_name = "config.yml"
    #     self.config_values : Dict[str, Any] = {}
    #     with open(self.config_file_name, 'r') as file:
    #          self.config_values = yaml.safe_load(file)

    #     self._load_defaults(self.config_values)
    
    # this is a Singleton class and this __new__ setup is at least one way to do it
    def __new__(cls):
        if(cls._instance is None):
            cls._instance = super(ConfigurationProcessor, cls).__new__(cls)
            cls.config_file_name = "config.yml"
            cls.config_values : Dict[str, Any] = {}
            with open(cls.config_file_name, 'r') as file:
                cls.config_values = yaml.safe_load(file)

            cls._load_defaults(cls.config_values)

        return cls._instance

    @classmethod
    def get_property(cls, val :str) -> Any:
        return cls.config_values[val]
    
    @classmethod
    def _load_defaults(cls, values : Dict[str, Any]) -> None:
        values["LOCALE"] = locale.LC_ALL
        debit_cats = list(values["DEBIT_CATEGORIES"])
        credit_cats = list(values["CREDIT_CATEGORIES"])
        values["CATEGORIES"] = cls._unique(debit_cats + credit_cats) 
        values["CATEGORIES_FOR_ADD"] = {"Debit": values["DEBIT_CATEGORIES"], "Credit": values["CREDIT_CATEGORIES"], "all": values["CATEGORIES"]}
        values["SIZE_LIST"] = [values["DATE_SIZE"], values["TRANS_SIZE"], values["CAT_SIZE"], values["DESC_SIZE"], values["AMOUNT_SIZE"], values["NUM_SIZE"]]
        values["MAX_WIDTH"] = sum(values["SIZE_LIST"]) + len(values["SIZE_LIST"]) + 1
        values["DEBIT_MULTIPLIER"] = -1


    @classmethod
    def _unique(cls, data_list: List[str]) -> List[str]:
        return_list: List[str] = []
        for cat in data_list:
            if cat not in return_list:
                return_list.append(cat)

        return return_list


if __name__ == "__main__":
    # print(ConfigurationProcessor().get_value("DATE_SIZE"))
    # print(ConfigurationProcessor().get_value("DEBIT_CATEGORIES"))


    for key, value in ConfigurationProcessor().config_values.items():
        print(key, ":", value, "->", type(value))
        # print(cp.get_value("CATEGORIES_FOR_ADD")["Debit"])
