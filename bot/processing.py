import json
from json import JSONDecodeError


class DataProcessor:

    TYPE_TABLE = {
        "data": str,
        "ricoverati_con_sintomi": int,
        "terapia_intensiva": int,
        "totale_ospedalizzati": int,
        "isolamento_domiciliare": int,
        "totale_positivi": int,
        "variazione_totale_positivi": int,
        "nuovi_positivi": int,
        "dimessi_guariti": int,
        "deceduti": int,
        "totale_casi": int,
        "tamponi": int
    }

    LOOKUP_TABLE = {
        "date": "data",
        "total_hospitalized_with_symptoms": "ricoverati_con_sintomi",
        "total_intensive_care": "terapia_intensiva",
        "total_hospitalized": "totale_ospedalizzati",
        "total_home_confinement": "isolamento_domiciliare",
        "total_active_positives": "totale_positivi",
        "delta_active_positives": "variazione_totale_positivi",
        "new_infected": "nuovi_positivi",
        "total_recovered": "dimessi_guariti",
        "total_deaths": "deceduti",
        "total_cases": "totale_casi",
        "total_tests": "tamponi"
    }

    def __init__(self, data):
        self.__data = data

    @staticmethod
    def initialize(data):
        final_data = data
        if not DataProcessor.__verify_data_structure(data):
            if isinstance(data, str) or isinstance(data, bytes) or isinstance(data, bytearray):
                try:
                    final_data = json.loads(data)
                except JSONDecodeError:
                    raise InvalidDataException(
                        "could not decode data (wrong format)")
                if not DataProcessor.__verify_data_structure(final_data):
                    raise InvalidDataException("invalid data structure")
            else:
                raise InvalidDataException("invalid data format")
        return DataProcessor(final_data)

    @staticmethod
    def __verify_data_structure(data):
        if not isinstance(data, list):
            return False
        for entry in data:
            if not isinstance(entry, dict):
                return False
            for key in DataProcessor.TYPE_TABLE.keys():
                if key not in entry:
                    return False
                if not isinstance(entry[key], DataProcessor.TYPE_TABLE[key]):
                    return False
        return True

    def get(self, key, start=None, end=None):
        start_from = start if start is not None else 0
        end_at = end if end is not None else self.size()
        actual_key = DataProcessor.LOOKUP_TABLE[key]
        values = list(map(lambda x: x[actual_key], self.__data))
        return values[start_from:end_at]

    def size(self):
        return len(self.__data)


class InvalidDataException(Exception):

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        if self.message:
            return "InvalidDataException: {0}".format(self.message)
        else:
            return "InvalidDataException: no message"
