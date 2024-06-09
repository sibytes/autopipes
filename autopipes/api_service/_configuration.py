import os
from . import autopipes_logging

_logger = autopipes_logging.get_logger(__name__)

"""
Loads the configuration from environment variables.

"""

def _get_databricks_secret(scope:str, key:str, default:str|None = None):
    from databricks.sdk.runtime import dbutils
    try:
        value = dbutils.secrets.get(scope, key)
        return value
    except Exception as e:
        value = os.getenv("SP_CLIENT_SECRET")

    if not value:
        value = default
    
    return value

_sp_schema = {
    "type": "object",
    "properties": {
        "auth_type": {
            "type": "string",
            "enum": [
                "MSAL",
                "SERVICE_PRINCIPAL"
            ],
        },
        "tenant_id": {"type": "string"},
        "sp_client_id": {"type": "string"},
        "sp_client_secret": {"type": "string"},
        "resource_group": {"type": "string"},
        "subcription_id": {"type": "string"}
    },
    "required": [
        "auth_type",
        "tenant_id",
        "sp_client_id",
        "sp_client_secret",
        "resource_group",
        "subcription_id"
    ],
}

databricks_scope = os.getenv("DATABRICKS_SCOPE")

if databricks_scope:
    from databricks.sdk.runtime import dbutils
    configuration = {
        "auth_type": _get_databricks_secret(databricks_scope, "AUTH_TYPE", "MSAL"),
        "tenant_id": _get_databricks_secret(databricks_scope, "TENANT_ID"),
        "sp_client_id": _get_databricks_secret(databricks_scope, "SP_CLIENT_ID"),
        "sp_client_secret": _get_databricks_secret(databricks_scope, "SP_CLIENT_SECRET"),
        "resource_group": _get_databricks_secret(databricks_scope, "RESOURCE_GROUP"), 
        "subscription_id": _get_databricks_secret(databricks_scope, "SUBSCRIPTION_ID"),
        "databricks_scope": databricks_scope
    }
else:


    configuration = {
        "auth_type": os.getenv("AUTH_TYPE", "MSAL"),
        "tenant_id": os.getenv("TENANT_ID"),
        "sp_client_id": os.getenv("SP_CLIENT_ID"),
        "sp_client_secret": os.getenv("SP_CLIENT_SECRET"),
        "resource_group": os.getenv("RESOURCE_GROUP"),
        "subscription_id": os.getenv("SUBSCRIPTION_ID")
    }
