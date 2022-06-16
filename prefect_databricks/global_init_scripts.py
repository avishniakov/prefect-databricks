"""
This is a module for interacting with Databricks REST tasks.
It was auto-generated using prefect-collection-generator so
manually editing this file is not recommended.
"""

from typing import TYPE_CHECKING, Any, Dict

from prefect import task

from prefect_databricks.rest import HTTPMethod, execute_endpoint

if TYPE_CHECKING:
    from prefect_databricks import DatabricksCredentials


@task
async def get_global_init_scripts(
    databricks_instance: str,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Get a list of all global init scripts for this workspace. This returns all
    properties for each script but **not** the script contents. To retrieve the
    contents of a script, use the [get a global init script](
    operation/get-script) operation.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.0/global-init-scripts?](
    https://{databricks_instance}/api/2.0/global-init-scripts?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Scripts were retrieved successfully. |
    | 403 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.0/global-init-scripts"  # noqa
    responses = {
        200: "Scripts were retrieved successfully.",  # noqa
        403: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    result = await execute_endpoint.fn(
        url,
        databricks_credentials,
        http_method=HTTPMethod.GET,
        responses=responses,
    )
    return result


@task
async def post_global_init_scripts(
    databricks_instance: str,
    enabled: str,
    name: str,
    position: str,
    script: str,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Create a new global init script in this workspace.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        enabled:
            Specifies whether the script is enabled. The script runs only if
            enabled.
        name:
            The name of the script, e.g. `My example script name`.
        position:
            The position of a global init script, where 0 represents the first
            global init script to run, 1 is the second global init
            script to run, and so on.  If you omit the position for a
            new global init script, it gets the last position. It runs
            after all current global init scripts. Setting any value
            greater than the position of the last script is equivalent
            to the last position. For example, suppose there are three
            existing scripts with positions 0, 1 and 2. Any position
            value of 3 or greater puts the script in the last position
            (3) If an explicit position value conflicts with an existing
            script, your request succeeds. The original script at that
            position and all later scripts have their position
            incremented by 1.
        script:
            The Base64-encoded content of the script, e.g. `ZWNobyBoZWxsbw==`.
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.0/global-init-scripts?](
    https://{databricks_instance}/api/2.0/global-init-scripts?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Script was created successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 403 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.0/global-init-scripts"  # noqa
    responses = {
        200: "Script was created successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        403: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    data = {
        "enabled": enabled,
        "name": name,
        "position": position,
        "script": script,
    }

    result = await execute_endpoint.fn(
        url,
        databricks_credentials,
        http_method=HTTPMethod.POST,
        responses=responses,
        data=data,
    )
    return result


@task
async def delete_global_init_scripts_script_id(
    databricks_instance: str,
    script_id: str,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Delete a global init script.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        script_id:
            Script id used in formatting the endpoint URL.
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.0/global-init-scripts/{script_id}?](
    https://{databricks_instance}/api/2.0/global-init-scripts/{script_id}?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | The script was deleted successfully. |
    | 403 | The request was unauthorized. |
    | 404 | The requested resource does not exist. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = (
        f"https://{databricks_instance}/api/2.0/global-init-scripts/{script_id}"  # noqa
    )
    responses = {
        200: "The script was deleted successfully.",  # noqa
        403: "The request was unauthorized.",  # noqa
        404: "The requested resource does not exist.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    result = await execute_endpoint.fn(
        url,
        databricks_credentials,
        http_method=HTTPMethod.DELETE,
        responses=responses,
    )
    return result


@task
async def get_global_init_scripts_script_id(
    databricks_instance: str,
    script_id: str,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Get all the details of a script, including its Base64-encoded contents.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        script_id:
            Script id used in formatting the endpoint URL.
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.0/global-init-scripts/{script_id}?](
    https://{databricks_instance}/api/2.0/global-init-scripts/{script_id}?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Script was retrieved successfully. |
    | 403 | The request was unauthorized. |
    | 404 | The requested resource does not exist. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = (
        f"https://{databricks_instance}/api/2.0/global-init-scripts/{script_id}"  # noqa
    )
    responses = {
        200: "Script was retrieved successfully.",  # noqa
        403: "The request was unauthorized.",  # noqa
        404: "The requested resource does not exist.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    result = await execute_endpoint.fn(
        url,
        databricks_credentials,
        http_method=HTTPMethod.GET,
        responses=responses,
    )
    return result


@task
async def patch_global_init_scripts_script_id(
    databricks_instance: str,
    script_id: str,
    enabled: str,
    name: str,
    position: str,
    script: str,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Update a global init script, specifying only the fields to change. All fields
    are optional. Unspecified fields retain their current value.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        script_id:
            Script id used in formatting the endpoint URL.
        enabled:
            Specifies whether the script is enabled. The script runs only if
            enabled.
        name:
            The name of the script, e.g. `My example script name`.
        position:
            The position of a script, where 0 represents the first script to run, 1
            is the second script to run, and so on.  To move the script
            so that it runs first, set its position to 0.  To move the
            script to the end, set it to any value greater or equal to
            the position of the last script. For example, suppose there
            are three existing scripts with positions 0, 1 and 2. Any
            position value of 2 or greater puts the script in the last
            position (2).  If an explicit position value conflicts with
            an existing script, your request succeeds. The original
            script at that position and all later scripts have their
            position incremented by 1.
        script:
            The Base64-encoded content of the script, e.g. `ZWNobyBoZWxsbw==`.
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.0/global-init-scripts/{script_id}?](
    https://{databricks_instance}/api/2.0/global-init-scripts/{script_id}?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | The script was updated successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 403 | The request was unauthorized. |
    | 404 | The requested resource does not exist. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = (
        f"https://{databricks_instance}/api/2.0/global-init-scripts/{script_id}"  # noqa
    )
    responses = {
        200: "The script was updated successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        403: "The request was unauthorized.",  # noqa
        404: "The requested resource does not exist.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    data = {
        "enabled": enabled,
        "name": name,
        "position": position,
        "script": script,
    }

    result = await execute_endpoint.fn(
        url,
        databricks_credentials,
        http_method=HTTPMethod.PATCH,
        responses=responses,
        data=data,
    )
    return result
