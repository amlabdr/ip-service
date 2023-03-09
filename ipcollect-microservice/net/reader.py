
class Reader:
    def __init__(self, config):
        self.config = config
        self.result = {}
        


    def __str__(self) -> str:
        return f'Reader = {vars(self)}'

    def read(self):
        raise NotImplementedError('Please use read in child class')

    def get_value(self, obj, keys, default_result=""):
        for key in keys:
            try:
                obj = obj[key]
            except KeyError:
                return default_result
        return obj


