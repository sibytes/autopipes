from ._auth_factory import auth_factory, AuthenticationType
from ._auth import Auth
from ._base_api import (
    base_api_get as _base_api_get,
    base_api_post as _base_api_post,
    base_api_delete as _base_api_delete,
    base_api_put as _base_api_put,
)
from . import autopipes_logging
from ._exceptions import AutopipesConfigurationInvalid, AutopipesResponseJsonError
from ._configuration import configuration
import json

_logger = autopipes_logging.get_logger(__name__)

class ApiService:
    def __init__(self, resource:str, config: dict = None):
        _logger.info("Initialising ApiService")

        self.resource = resource
        if config:
            _logger.debug("Configuring ApiService from constructor")
            _config = config
        else:
            _logger.debug("Configuring ApiService from default configuration")
            _config = configuration

        config_json = json.dumps(_config, indent=4)
        _logger.debug(config_json)

        try:
            auth_type_str = _config["auth_type"]
        except KeyError:
            e = AutopipesConfigurationInvalid(
                "auth_type", valid_values=AuthenticationType
            )
            _logger.error(e.message)
            raise e

        try:
            self.subscription_id = _config["subscription_id"]
        except KeyError:
            e = AutopipesConfigurationInvalid("subscription_id")
            _logger.error(e.message)
            raise e
        
        try:
            self.resource_group = _config["resource_group"]
        except KeyError:
            e = AutopipesConfigurationInvalid("resource_group")
            _logger.error(e.message)
            raise e
        
        _config["resource"] = self.resource
        
        
        self.host = f"{self.resource}/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}"


        try:
            _logger.debug(f"Setting AuthorisationType as {auth_type_str}")
            self.auth_type: AuthenticationType = AuthenticationType[auth_type_str]
        except Exception:
            e = AutopipesConfigurationInvalid(
                "auth_type", value=auth_type_str, valid_values=AuthenticationType
            )
            _logger.error(e.message)
            raise e

        auth: Auth = auth_factory.get_auth(self.auth_type, _config)

        _logger.debug("Setting Authorisation Headers")
        self._headers = auth.get_headers()
        _header_json = json.dumps(self._headers, indent=4)
        _logger.debug(_header_json)

    def api_put(
        self,
        endpoint: str,
        data: dict = None,
        params=None
    ):

        url = f"{self.host}/{endpoint}"

        response = _base_api_put(
            url=url, headers=self._headers, json=data, params=params
        )

        try:
            json = response.json()
        except Exception:
            ex = AutopipesResponseJsonError(url, "PUT", data, response.text)
            _logger.error(ex.message)
            raise ex

        return json

    def api_get(
        self,
        endpoint: str,
        data: dict = None,
        params=None
    ):
        url = f"{self.host}/{endpoint}"

        response = _base_api_get(
            url=url, headers=self._headers, json=data, params=params
        )

        try:
            json = response.json()
        except Exception:
            ex = AutopipesResponseJsonError(url, "GET", data, response.text)
            _logger.error(ex.message)
            raise ex

        return json

    def api_delete(
        self,
        endpoint: str,
        data: dict = None,
        params=None
    ):
        url = f"{self.host}/{endpoint}"

        response = _base_api_delete(
            url=url, headers=self._headers, json=data, params=params
        )

        try:
            json = response.json()
        except Exception:
            ex = AutopipesResponseJsonError(url, "DELETE", data, response.text)
            _logger.error(ex.message)
            raise ex

        return json

    def api_post(
        self,
        endpoint: str,
        data: dict = None
    ):
        url = f"{self.host}/{endpoint}"

        response = _base_api_post(url=url, headers=self._headers, json=data)

        try:
            json = response.json()
        except Exception:
            ex = AutopipesResponseJsonError(url, "POST", data, response.text)
            _logger.error(ex.message)
            raise ex

        return json
