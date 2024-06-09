from .api_service import ApiService, autopipes_logging
from typing import Union

_logger = autopipes_logging.get_logger(__name__)

_ADF_API_VERSION = "2018-06-01"
_endpoint = "providers/Microsoft.DataFactory/factories"

_api_service = ApiService(resource="https://management.azure.com")


class DataFactoryPipelineException(Exception):
    def __init__(self, name: Union[str, int]):
        if isinstance(name, int):
            msg = f"Failed on pipeline job_id={name}"
        else:
            msg = f"Failed on pipeline name={name}"

        self.message = msg
        super().__init__(self.message)


def pipeline_create_run(
        pipeline:str,
        datafactory: str,
        parameters: dict | None = None
):
    endpoint  = f"{_endpoint}/{datafactory}/pipelines/{pipeline}/createRun?api-version={_ADF_API_VERSION}"
    try:
        response = _api_service.api_post(endpoint)
        run_id = response["runId"]
        response["url"] = f"https://adf.azure.com/en/monitoring/pipelineruns/{run_id}?factory=%2Fsubscriptions%2F{_api_service.subscription_id}%2FresourceGroups%2F{_api_service.resource_group}%2Fproviders%2FMicrosoft.DataFactory%2Ffactories%2F{datafactory}"
    except Exception:
        raise DataFactoryPipelineException(pipeline)

    return response
