import enum
import json


class AutopipesResponseJsonError(Exception):
    def __init__(self, verb: str, url: str, data: dict, response_text: str):
        _data = json.dumps(data, indent=4)
        self.message = f"HTTP {verb} response.json() from {url} failed. request_body= {_data}. response.text={response_text}"
        super().__init__(self.message)


class AutopipesConfigurationInvalid(Exception):
    def __init__(
        self,
        configuration_variable: str,
        value: str = None,
        valid_values: enum.Enum = None,
    ):
        self.message = f"Autopipes configuration variable '{configuration_variable}' is not valid. {configuration_variable}={value}."
        if valid_values:
            values = ", ".join([v.name for v in valid_values])
            self.message = f"{self.message} Valid values are: {values}"
        super().__init__(self.message)


class AutopipesAuthTypeNotRegistered(Exception):
    def __init__(self, auth_type: enum.Enum):
        self.message = f"Autopipes authentication type {auth_type.name} has not been registered in the AuthFactory module"
        super().__init__(self.message)
