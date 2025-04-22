class DataStorage:
    def __init__(self):
        self.descriptions = []
        self.dataframes = {}
        self.jsons = {}
        self.calls = []

    def store(self, data_dict):
        description = data_dict["description"]
        call = data_dict["call"]

        self.descriptions.append(description)
        self.calls.append(call)
        if "dataframe" in data_dict:
            self.dataframes[description] = data_dict["dataframe"]
        if "json" in data_dict:
            self.jsons[description] = data_dict["json"]

    def get_catalogue(self) -> list:
        return self.descriptions
    
    def get_calls(self):
        return self.calls

    def get_list(self, type: str) -> list:
        if type == "dataframe":
            return self.dataframes.values()
        elif type == "json":
            return self.jsons.values()
        
    def __len__(self) -> bool:
        return len(self.descriptions)
        