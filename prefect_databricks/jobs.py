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
async def post_2_1_jobs_create(
    databricks_instance: str,
    tasks: list,
    job_clusters: list,
    email_notifications: str,
    timeout_seconds: int,
    schedule: str,
    max_concurrent_runs: int,
    git_source: str,
    format: str,
    access_control_list: list,
    databricks_credentials: "DatabricksCredentials",
    name: str = "Untitled",
    tags: dict = None,
) -> Dict[str, Any]:
    """
    Create a new job.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        tasks:
            A list of task specifications to be executed by this job, e.g.
            ```
            [
                {
                    "task_key": "Sessionize",
                    "description": "Extracts session data from events",
                    "depends_on": [],
                    "existing_cluster_id": "0923-164208-meows279",
                    "spark_jar_task": {
                        "main_class_name": "com.databricks.Sessionize",
                        "parameters": ["--data", "dbfs:/path/to/data.json"],
                    },
                    "libraries": [{"jar": "dbfs:/mnt/databricks/Sessionize.jar"}],
                    "timeout_seconds": 86400,
                    "max_retries": 3,
                    "min_retry_interval_millis": 2000,
                    "retry_on_timeout": False,
                },
                {
                    "task_key": "Orders_Ingest",
                    "description": "Ingests order data",
                    "depends_on": [],
                    "job_cluster_key": "auto_scaling_cluster",
                    "spark_jar_task": {
                        "main_class_name": "com.databricks.OrdersIngest",
                        "parameters": ["--data", "dbfs:/path/to/order-data.json"],
                    },
                    "libraries": [{"jar": "dbfs:/mnt/databricks/OrderIngest.jar"}],
                    "timeout_seconds": 86400,
                    "max_retries": 3,
                    "min_retry_interval_millis": 2000,
                    "retry_on_timeout": False,
                },
                {
                    "task_key": "Match",
                    "description": "Matches orders with user sessions",
                    "depends_on": [
                        {"task_key": "Orders_Ingest"},
                        {"task_key": "Sessionize"},
                    ],
                    "new_cluster": {
                        "spark_version": "7.3.x-scala2.12",
                        "node_type_id": "i3.xlarge",
                        "spark_conf": {"spark.speculation": True},
                        "aws_attributes": {
                            "availability": "SPOT",
                            "zone_id": "us-west-2a",
                        },
                        "autoscale": {"min_workers": 2, "max_workers": 16},
                    },
                    "notebook_task": {
                        "notebook_path": "/Users/user.name@databricks.com/Match",
                        "base_parameters": {"name": "John Doe", "age": "35"},
                    },
                    "timeout_seconds": 86400,
                    "max_retries": 3,
                    "min_retry_interval_millis": 2000,
                    "retry_on_timeout": False,
                },
            ]
            ```
        job_clusters:
            A list of job cluster specifications that can be shared and reused by
            tasks of this job. Libraries cannot be declared in a shared
            job cluster. You must declare dependent libraries in task
            settings, e.g.
            ```
            [
                {
                    "job_cluster_key": "auto_scaling_cluster",
                    "new_cluster": {
                        "spark_version": "7.3.x-scala2.12",
                        "node_type_id": "i3.xlarge",
                        "spark_conf": {"spark.speculation": True},
                        "aws_attributes": {
                            "availability": "SPOT",
                            "zone_id": "us-west-2a",
                        },
                        "autoscale": {"min_workers": 2, "max_workers": 16},
                    },
                }
            ]
            ```
        email_notifications:
            An optional set of email addresses that is notified when runs of this
            job begin or complete as well as when this job is deleted.
            The default behavior is to not send any emails. Key-values:
            - on_start:
                A list of email addresses to be notified when a run begins.
                If not specified on job creation, reset, or update, the list
                is empty, and notifications are not sent, e.g.
                ```
                ["user.name@databricks.com"]
                ```
            - on_success:
                A list of email addresses to be notified when a run
                successfully completes. A run is considered to have
                completed successfully if it ends with a `TERMINATED`
                `life_cycle_state` and a `SUCCESSFUL` result_state. If not
                specified on job creation, reset, or update, the list is
                empty, and notifications are not sent, e.g.
                ```
                ["user.name@databricks.com"]
                ```
            - on_failure:
                A list of email addresses to be notified when a run
                unsuccessfully completes. A run is considered to have
                completed unsuccessfully if it ends with an `INTERNAL_ERROR`
                `life_cycle_state` or a `SKIPPED`, `FAILED`, or `TIMED_OUT`
                result_state. If this is not specified on job creation,
                reset, or update the list is empty, and notifications are
                not sent, e.g.
                ```
                ["user.name@databricks.com"]
                ```
            - no_alert_for_skipped_runs:
                If true, do not send email to recipients specified in
                `on_failure` if the run is skipped.
        timeout_seconds:
            An optional timeout applied to each run of this job. The default
            behavior is to have no timeout, e.g. `86400`.
        schedule:
            An optional periodic schedule for this job. The default behavior is that
            the job only runs when triggered by clicking “Run Now” in
            the Jobs UI or sending an API request to `runNow`. Key-values:
            - quartz_cron_expression:
                A Cron expression using Quartz syntax that describes the
                schedule for a job. See [Cron Trigger](http://www.quartz-
                scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html)
                for details. This field is required, e.g. `20 30 * * * ?`.
            - timezone_id:
                A Java timezone ID. The schedule for a job is resolved with
                respect to this timezone. See [Java
                TimeZone](https://docs.oracle.com/javase/7/docs/api/java/util/TimeZone.html)
                for details. This field is required, e.g. `Europe/London`.
            - pause_status:
                Indicate whether this schedule is paused or not, e.g.
                `PAUSED`.
        max_concurrent_runs:
            An optional maximum allowed number of concurrent runs of the job.  Set
            this value if you want to be able to execute multiple runs
            of the same job concurrently. This is useful for example if
            you trigger your job on a frequent schedule and want to
            allow consecutive runs to overlap with each other, or if you
            want to trigger multiple runs which differ by their input
            parameters.  This setting affects only new runs. For
            example, suppose the job’s concurrency is 4 and there are 4
            concurrent active runs. Then setting the concurrency to 3
            won’t kill any of the active runs. However, from then on,
            new runs are skipped unless there are fewer than 3 active
            runs.  This value cannot exceed 1000\. Setting this value to
            0 causes all new runs to be skipped. The default behavior is
            to allow only 1 concurrent run, e.g. `10`.
        git_source:
            This functionality is in Public Preview.  An optional specification for
            a remote repository containing the notebooks used by this
            job's notebook tasks. Key-values:
            - git_url:
                URL of the repository to be cloned by this job. The maximum
                length is 300 characters, e.g.
                `https://github.com/databricks/databricks-cli`.
            - git_provider:
                Unique identifier of the service used to host the Git
                repository. The value is case insensitive, e.g. `github`.
            - git_branch:
                Name of the branch to be checked out and used by this job.
                This field cannot be specified in conjunction with git_tag
                or git_commit. The maximum length is 255 characters, e.g.
                `main`.
            - git_tag:
                Name of the tag to be checked out and used by this job. This
                field cannot be specified in conjunction with git_branch or
                git_commit. The maximum length is 255 characters, e.g.
                `release-1.0.0`.
            - git_commit:
                Commit to be checked out and used by this job. This field
                cannot be specified in conjunction with git_branch or
                git_tag. The maximum length is 64 characters, e.g.
                `e0056d01`.
            - git_snapshot:
                Read-only state of the remote repository at the time the job was run.
                            This field is only included on job runs.
        format:
            Used to tell what is the format of the job. This field is ignored in
            Create/Update/Reset calls. When using the Jobs API 2.1 this
            value is always set to `"MULTI_TASK"`, e.g. `MULTI_TASK`.
        access_control_list:
            List of permissions to set on the job.
        databricks_credentials:
            Credentials to use for authentication with Databricks.
        name:
            An optional name for the job, e.g. `A multitask job`.
        tags:
            A map of tags associated with the job. These are forwarded to the
            cluster as cluster tags for jobs clusters, and are subject
            to the same limitations as cluster tags. A maximum of 25
            tags can be added to the job, e.g.
            ```
            {"cost-center": "engineering", "team": "jobs"}
            ```

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/create?](
    https://{databricks_instance}/api/2.1/jobs/create?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Job was created successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/create"  # noqa
    responses = {
        200: "Job was created successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    data = {
        "name": name,
        "tags": tags,
        "tasks": tasks,
        "job_clusters": job_clusters,
        "email_notifications": email_notifications,
        "timeout_seconds": timeout_seconds,
        "schedule": schedule,
        "max_concurrent_runs": max_concurrent_runs,
        "git_source": git_source,
        "format": format,
        "access_control_list": access_control_list,
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
async def get_2_1_jobs_list(
    databricks_instance: str,
    databricks_credentials: "DatabricksCredentials",
    limit: int = 20,
    offset: int = 0,
    expand_tasks: bool = False,
) -> Dict[str, Any]:
    """
    Retrieves a list of jobs.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        databricks_credentials:
            Credentials to use for authentication with Databricks.
        limit:
            The number of jobs to return. This value must be greater than 0 and less
            or equal to 25. The default value is 20.
        offset:
            The offset of the first job to return, relative to the most recently
            created job.
        expand_tasks:
            Whether to include task and cluster details in the response.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/list?&limit=%s&offset=%s&expand_tasks=%s](
    https://{databricks_instance}/api/2.1/jobs/list?&limit=%s&offset=%s&expand_tasks=%s)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | List of jobs was retrieved successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/list"  # noqa
    responses = {
        200: "List of jobs was retrieved successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    params = {
        "limit": limit,
        "offset": offset,
        "expand_tasks": expand_tasks,
    }

    result = await execute_endpoint.fn(
        url,
        databricks_credentials,
        http_method=HTTPMethod.GET,
        params=params,
        responses=responses,
    )
    return result


@task
async def get_2_1_jobs_get(
    databricks_instance: str,
    job_id: int,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Retrieves the details for a single job.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        job_id:
            The canonical identifier of the job to retrieve information about. This
            field is required.
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/get?&job_id=%s](
    https://{databricks_instance}/api/2.1/jobs/get?&job_id=%s)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Job was retrieved successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/get"  # noqa
    responses = {
        200: "Job was retrieved successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    params = {
        "job_id": job_id,
    }

    result = await execute_endpoint.fn(
        url,
        databricks_credentials,
        http_method=HTTPMethod.GET,
        params=params,
        responses=responses,
    )
    return result


@task
async def post_2_1_jobs_reset(
    databricks_instance: str,
    job_id: int,
    new_settings: str,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Overwrites all the settings for a specific job. Use the Update endpoint to
    update job settings partially.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        job_id:
            The canonical identifier of the job to reset. This field is required,
            e.g. `11223344`.
        new_settings:
            The new settings of the job. These settings completely replace the old
            settings.  Changes to the field
            `JobSettings.timeout_seconds` are applied to active runs.
            Changes to other fields are applied to future runs only. Key-values:
            - name:
                An optional name for the job, e.g. `A multitask job`.
            - tags:
                A map of tags associated with the job. These are forwarded
                to the cluster as cluster tags for jobs clusters, and are
                subject to the same limitations as cluster tags. A maximum
                of 25 tags can be added to the job, e.g.
                ```
                {"cost-center": "engineering", "team": "jobs"}
                ```
            - tasks:
                A list of task specifications to be executed by this job, e.g.
                ```
                [
                    {
                        "task_key": "Sessionize",
                        "description": "Extracts session data from events",
                        "depends_on": [],
                        "existing_cluster_id": "0923-164208-meows279",
                        "spark_jar_task": {
                            "main_class_name": "com.databricks.Sessionize",
                            "parameters": [
                                "--data",
                                "dbfs:/path/to/data.json",
                            ],
                        },
                        "libraries": [
                            {"jar": "dbfs:/mnt/databricks/Sessionize.jar"}
                        ],
                        "timeout_seconds": 86400,
                        "max_retries": 3,
                        "min_retry_interval_millis": 2000,
                        "retry_on_timeout": False,
                    },
                    {
                        "task_key": "Orders_Ingest",
                        "description": "Ingests order data",
                        "depends_on": [],
                        "job_cluster_key": "auto_scaling_cluster",
                        "spark_jar_task": {
                            "main_class_name": "com.databricks.OrdersIngest",
                            "parameters": [
                                "--data",
                                "dbfs:/path/to/order-data.json",
                            ],
                        },
                        "libraries": [
                            {"jar": "dbfs:/mnt/databricks/OrderIngest.jar"}
                        ],
                        "timeout_seconds": 86400,
                        "max_retries": 3,
                        "min_retry_interval_millis": 2000,
                        "retry_on_timeout": False,
                    },
                    {
                        "task_key": "Match",
                        "description": "Matches orders with user sessions",
                        "depends_on": [
                            {"task_key": "Orders_Ingest"},
                            {"task_key": "Sessionize"},
                        ],
                        "new_cluster": {
                            "spark_version": "7.3.x-scala2.12",
                            "node_type_id": "i3.xlarge",
                            "spark_conf": {"spark.speculation": True},
                            "aws_attributes": {
                                "availability": "SPOT",
                                "zone_id": "us-west-2a",
                            },
                            "autoscale": {
                                "min_workers": 2,
                                "max_workers": 16,
                            },
                        },
                        "notebook_task": {
                            "notebook_path": "/Users/user.name@databricks.com/Match",
                            "base_parameters": {
                                "name": "John Doe",
                                "age": "35",
                            },
                        },
                        "timeout_seconds": 86400,
                        "max_retries": 3,
                        "min_retry_interval_millis": 2000,
                        "retry_on_timeout": False,
                    },
                ]
                ```
            - job_clusters:
                A list of job cluster specifications that can be shared and
                reused by tasks of this job. Libraries cannot be declared in
                a shared job cluster. You must declare dependent libraries
                in task settings, e.g.
                ```
                [
                    {
                        "job_cluster_key": "auto_scaling_cluster",
                        "new_cluster": {
                            "spark_version": "7.3.x-scala2.12",
                            "node_type_id": "i3.xlarge",
                            "spark_conf": {"spark.speculation": True},
                            "aws_attributes": {
                                "availability": "SPOT",
                                "zone_id": "us-west-2a",
                            },
                            "autoscale": {
                                "min_workers": 2,
                                "max_workers": 16,
                            },
                        },
                    }
                ]
                ```
            - email_notifications:
                An optional set of email addresses that is notified when
                runs of this job begin or complete as well as when this job
                is deleted. The default behavior is to not send any emails.
            - timeout_seconds:
                An optional timeout applied to each run of this job. The
                default behavior is to have no timeout, e.g. `86400`.
            - schedule:
                An optional periodic schedule for this job. The default
                behavior is that the job only runs when triggered by
                clicking “Run Now” in the Jobs UI or sending an API request
                to `runNow`.
            - max_concurrent_runs:
                An optional maximum allowed number of concurrent runs of the
                job.  Set this value if you want to be able to execute
                multiple runs of the same job concurrently. This is useful
                for example if you trigger your job on a frequent schedule
                and want to allow consecutive runs to overlap with each
                other, or if you want to trigger multiple runs which differ
                by their input parameters.  This setting affects only new
                runs. For example, suppose the job’s concurrency is 4 and
                there are 4 concurrent active runs. Then setting the
                concurrency to 3 won’t kill any of the active runs. However,
                from then on, new runs are skipped unless there are fewer
                than 3 active runs.  This value cannot exceed 1000\. Setting
                this value to 0 causes all new runs to be skipped. The
                default behavior is to allow only 1 concurrent run, e.g.
                `10`.
            - git_source:
                This functionality is in Public Preview.  An optional
                specification for a remote repository containing the
                notebooks used by this job's notebook tasks.
            - format:
                Used to tell what is the format of the job. This field is
                ignored in Create/Update/Reset calls. When using the Jobs
                API 2.1 this value is always set to `"MULTI_TASK"`, e.g.
                `MULTI_TASK`.
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/reset?](
    https://{databricks_instance}/api/2.1/jobs/reset?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Job was overwritten successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/reset"  # noqa
    responses = {
        200: "Job was overwritten successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    data = {
        "job_id": job_id,
        "new_settings": new_settings,
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
async def post_2_1_jobs_update(
    databricks_instance: str,
    job_id: int,
    new_settings: str,
    fields_to_remove: list,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Add, update, or remove specific settings of an existing job. Use the Reset
    endpoint to overwrite all job settings.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        job_id:
            The canonical identifier of the job to update. This field is required,
            e.g. `11223344`.
        new_settings:
            The new settings for the job. Any top-level fields specified in
            `new_settings` are completely replaced. Partially updating
            nested fields is not supported.  Changes to the field
            `JobSettings.timeout_seconds` are applied to active runs.
            Changes to other fields are applied to future runs only. Key-values:
            - name:
                An optional name for the job, e.g. `A multitask job`.
            - tags:
                A map of tags associated with the job. These are forwarded
                to the cluster as cluster tags for jobs clusters, and are
                subject to the same limitations as cluster tags. A maximum
                of 25 tags can be added to the job, e.g.
                ```
                {"cost-center": "engineering", "team": "jobs"}
                ```
            - tasks:
                A list of task specifications to be executed by this job, e.g.
                ```
                [
                    {
                        "task_key": "Sessionize",
                        "description": "Extracts session data from events",
                        "depends_on": [],
                        "existing_cluster_id": "0923-164208-meows279",
                        "spark_jar_task": {
                            "main_class_name": "com.databricks.Sessionize",
                            "parameters": [
                                "--data",
                                "dbfs:/path/to/data.json",
                            ],
                        },
                        "libraries": [
                            {"jar": "dbfs:/mnt/databricks/Sessionize.jar"}
                        ],
                        "timeout_seconds": 86400,
                        "max_retries": 3,
                        "min_retry_interval_millis": 2000,
                        "retry_on_timeout": False,
                    },
                    {
                        "task_key": "Orders_Ingest",
                        "description": "Ingests order data",
                        "depends_on": [],
                        "job_cluster_key": "auto_scaling_cluster",
                        "spark_jar_task": {
                            "main_class_name": "com.databricks.OrdersIngest",
                            "parameters": [
                                "--data",
                                "dbfs:/path/to/order-data.json",
                            ],
                        },
                        "libraries": [
                            {"jar": "dbfs:/mnt/databricks/OrderIngest.jar"}
                        ],
                        "timeout_seconds": 86400,
                        "max_retries": 3,
                        "min_retry_interval_millis": 2000,
                        "retry_on_timeout": False,
                    },
                    {
                        "task_key": "Match",
                        "description": "Matches orders with user sessions",
                        "depends_on": [
                            {"task_key": "Orders_Ingest"},
                            {"task_key": "Sessionize"},
                        ],
                        "new_cluster": {
                            "spark_version": "7.3.x-scala2.12",
                            "node_type_id": "i3.xlarge",
                            "spark_conf": {"spark.speculation": True},
                            "aws_attributes": {
                                "availability": "SPOT",
                                "zone_id": "us-west-2a",
                            },
                            "autoscale": {
                                "min_workers": 2,
                                "max_workers": 16,
                            },
                        },
                        "notebook_task": {
                            "notebook_path": "/Users/user.name@databricks.com/Match",
                            "base_parameters": {
                                "name": "John Doe",
                                "age": "35",
                            },
                        },
                        "timeout_seconds": 86400,
                        "max_retries": 3,
                        "min_retry_interval_millis": 2000,
                        "retry_on_timeout": False,
                    },
                ]
                ```
            - job_clusters:
                A list of job cluster specifications that can be shared and
                reused by tasks of this job. Libraries cannot be declared in
                a shared job cluster. You must declare dependent libraries
                in task settings, e.g.
                ```
                [
                    {
                        "job_cluster_key": "auto_scaling_cluster",
                        "new_cluster": {
                            "spark_version": "7.3.x-scala2.12",
                            "node_type_id": "i3.xlarge",
                            "spark_conf": {"spark.speculation": True},
                            "aws_attributes": {
                                "availability": "SPOT",
                                "zone_id": "us-west-2a",
                            },
                            "autoscale": {
                                "min_workers": 2,
                                "max_workers": 16,
                            },
                        },
                    }
                ]
                ```
            - email_notifications:
                An optional set of email addresses that is notified when
                runs of this job begin or complete as well as when this job
                is deleted. The default behavior is to not send any emails.
            - timeout_seconds:
                An optional timeout applied to each run of this job. The
                default behavior is to have no timeout, e.g. `86400`.
            - schedule:
                An optional periodic schedule for this job. The default
                behavior is that the job only runs when triggered by
                clicking “Run Now” in the Jobs UI or sending an API request
                to `runNow`.
            - max_concurrent_runs:
                An optional maximum allowed number of concurrent runs of the
                job.  Set this value if you want to be able to execute
                multiple runs of the same job concurrently. This is useful
                for example if you trigger your job on a frequent schedule
                and want to allow consecutive runs to overlap with each
                other, or if you want to trigger multiple runs which differ
                by their input parameters.  This setting affects only new
                runs. For example, suppose the job’s concurrency is 4 and
                there are 4 concurrent active runs. Then setting the
                concurrency to 3 won’t kill any of the active runs. However,
                from then on, new runs are skipped unless there are fewer
                than 3 active runs.  This value cannot exceed 1000\. Setting
                this value to 0 causes all new runs to be skipped. The
                default behavior is to allow only 1 concurrent run, e.g.
                `10`.
            - git_source:
                This functionality is in Public Preview.  An optional
                specification for a remote repository containing the
                notebooks used by this job's notebook tasks.
            - format:
                Used to tell what is the format of the job. This field is
                ignored in Create/Update/Reset calls. When using the Jobs
                API 2.1 this value is always set to `"MULTI_TASK"`, e.g.
                `MULTI_TASK`.
        fields_to_remove:
            Remove top-level fields in the job settings. Removing nested fields is
            not supported. This field is optional, e.g.
            ```
            ["libraries", "schedule"]
            ```
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/update?](
    https://{databricks_instance}/api/2.1/jobs/update?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Job was updated successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/update"  # noqa
    responses = {
        200: "Job was updated successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    data = {
        "job_id": job_id,
        "new_settings": new_settings,
        "fields_to_remove": fields_to_remove,
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
async def post_2_1_jobs_delete(
    databricks_instance: str,
    job_id: int,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Deletes a job.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        job_id:
            The canonical identifier of the job to delete. This field is required,
            e.g. `11223344`.
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/delete?](
    https://{databricks_instance}/api/2.1/jobs/delete?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Job was deleted successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/delete"  # noqa
    responses = {
        200: "Job was deleted successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    data = {
        "job_id": job_id,
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
async def post_2_1_jobs_run_now(
    databricks_instance: str,
    job_id: int,
    idempotency_token: str,
    jar_params: list,
    notebook_params: dict,
    python_params: list,
    spark_submit_params: list,
    python_named_params: dict,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Run a job and return the `run_id` of the triggered run.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        job_id:
            The ID of the job to be executed, e.g. `11223344`.
        idempotency_token:
            An optional token to guarantee the idempotency of job run requests. If a
            run with the provided token already exists, the request does
            not create a new run but returns the ID of the existing run
            instead.  If you specify the idempotency token, upon failure
            you can retry until the request succeeds. Databricks
            guarantees that exactly one run is launched with that
            idempotency token.  This token must have at most 64
            characters.  For more information, see [How to ensure
            idempotency for jobs](https://kb.databricks.com/jobs/jobs-
            idempotency.html), e.g.
            `8f018174-4792-40d5-bcbc-3e6a527352c8`.
        jar_params:
            A list of parameters for jobs with Spark JAR tasks, for example
            `"jar_params": ["john doe", "35"]`. The parameters are used
            to invoke the main function of the main class specified in
            the Spark JAR task. If not specified upon `run-now`, it
            defaults to an empty list. jar_params cannot be specified in
            conjunction with notebook_params. The JSON representation of
            this field (for example `{"jar_params":["john doe","35"]}`)
            cannot exceed 10,000 bytes.  Use [Task parameter
            variables](https://docs.databricks.com/jobs.html
            parameter-variables) to set parameters containing
            information about job runs, e.g.
            ```
            ["john", "doe", "35"]
            ```
        notebook_params:
            A map from keys to values for jobs with notebook task, for example
            `"notebook_params": {"name": "john doe", "age": "35"}`. The
            map is passed to the notebook and is accessible through the
            [dbutils.widgets.get](https://docs.databricks.com/dev-
            tools/databricks-utils.html
            dbutils-widgets) function.  If not specified upon `run-now`,
            the triggered run uses the job’s base parameters.
            notebook_params cannot be specified in conjunction with
            jar_params.  Use [Task parameter
            variables](https://docs.databricks.com/jobs.html
            parameter-variables) to set parameters containing
            information about job runs.  The JSON representation of this
            field (for example `{"notebook_params":{"name":"john
            doe","age":"35"}}`) cannot exceed 10,000 bytes, e.g.
            ```
            {"name": "john doe", "age": "35"}
            ```
        python_params:
            A list of parameters for jobs with Python tasks, for example
            `"python_params": ["john doe", "35"]`. The parameters are
            passed to Python file as command-line parameters. If
            specified upon `run-now`, it would overwrite the parameters
            specified in job setting. The JSON representation of this
            field (for example `{"python_params":["john doe","35"]}`)
            cannot exceed 10,000 bytes.  Use [Task parameter
            variables](https://docs.databricks.com/jobs.html
            parameter-variables) to set parameters containing
            information about job runs.  Important  These parameters
            accept only Latin characters (ASCII character set). Using
            non-ASCII characters returns an error. Examples of invalid,
            non-ASCII characters are Chinese, Japanese kanjis, and
            emojis, e.g.
            ```
            ["john doe", "35"]
            ```
        spark_submit_params:
            A list of parameters for jobs with spark submit task, for example
            `"spark_submit_params": ["--class",
            "org.apache.spark.examples.SparkPi"]`. The parameters are
            passed to spark-submit script as command-line parameters. If
            specified upon `run-now`, it would overwrite the parameters
            specified in job setting. The JSON representation of this
            field (for example `{"python_params":["john doe","35"]}`)
            cannot exceed 10,000 bytes.  Use [Task parameter
            variables](https://docs.databricks.com/jobs.html
            parameter-variables) to set parameters containing
            information about job runs.  Important  These parameters
            accept only Latin characters (ASCII character set). Using
            non-ASCII characters returns an error. Examples of invalid,
            non-ASCII characters are Chinese, Japanese kanjis, and
            emojis, e.g.
            ```
            ["--class", "org.apache.spark.examples.SparkPi"]
            ```
        python_named_params:
            A map from keys to values for jobs with Python wheel task, for example
            `"python_named_params": {"name": "task", "data":
            "dbfs:/path/to/data.json"}`, e.g.
            ```
            {"name": "task", "data": "dbfs:/path/to/data.json"}
            ```
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/run-now?](
    https://{databricks_instance}/api/2.1/jobs/run-now?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Run was started successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/run-now"  # noqa
    responses = {
        200: "Run was started successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    data = {
        "job_id": job_id,
        "idempotency_token": idempotency_token,
        "jar_params": jar_params,
        "notebook_params": notebook_params,
        "python_params": python_params,
        "spark_submit_params": spark_submit_params,
        "python_named_params": python_named_params,
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
async def post_2_1_jobs_runs_submit(
    databricks_instance: str,
    tasks: list,
    run_name: str,
    git_source: str,
    timeout_seconds: int,
    idempotency_token: str,
    access_control_list: list,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Submit a one-time run. This endpoint allows you to submit a workload directly
    without creating a job. Runs submitted using this endpoint don’t display in
    the UI. Use the `jobs/runs/get` API to check the run state after the job is
    submitted.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        tasks:
            , e.g.
            ```
            [
                {
                    "task_key": "Sessionize",
                    "description": "Extracts session data from events",
                    "depends_on": [],
                    "existing_cluster_id": "0923-164208-meows279",
                    "spark_jar_task": {
                        "main_class_name": "com.databricks.Sessionize",
                        "parameters": ["--data", "dbfs:/path/to/data.json"],
                    },
                    "libraries": [{"jar": "dbfs:/mnt/databricks/Sessionize.jar"}],
                    "timeout_seconds": 86400,
                },
                {
                    "task_key": "Orders_Ingest",
                    "description": "Ingests order data",
                    "depends_on": [],
                    "existing_cluster_id": "0923-164208-meows279",
                    "spark_jar_task": {
                        "main_class_name": "com.databricks.OrdersIngest",
                        "parameters": ["--data", "dbfs:/path/to/order-data.json"],
                    },
                    "libraries": [{"jar": "dbfs:/mnt/databricks/OrderIngest.jar"}],
                    "timeout_seconds": 86400,
                },
                {
                    "task_key": "Match",
                    "description": "Matches orders with user sessions",
                    "depends_on": [
                        {"task_key": "Orders_Ingest"},
                        {"task_key": "Sessionize"},
                    ],
                    "new_cluster": {
                        "spark_version": "7.3.x-scala2.12",
                        "node_type_id": "i3.xlarge",
                        "spark_conf": {"spark.speculation": True},
                        "aws_attributes": {
                            "availability": "SPOT",
                            "zone_id": "us-west-2a",
                        },
                        "autoscale": {"min_workers": 2, "max_workers": 16},
                    },
                    "notebook_task": {
                        "notebook_path": "/Users/user.name@databricks.com/Match",
                        "base_parameters": {"name": "John Doe", "age": "35"},
                    },
                    "timeout_seconds": 86400,
                },
            ]
            ```
        run_name:
            An optional name for the run. The default value is `Untitled`, e.g. `A
            multitask job run`.
        git_source:
            This functionality is in Public Preview.  An optional specification for
            a remote repository containing the notebooks used by this
            job's notebook tasks. Key-values:
            - git_url:
                URL of the repository to be cloned by this job. The maximum
                length is 300 characters, e.g.
                `https://github.com/databricks/databricks-cli`.
            - git_provider:
                Unique identifier of the service used to host the Git
                repository. The value is case insensitive, e.g. `github`.
            - git_branch:
                Name of the branch to be checked out and used by this job.
                This field cannot be specified in conjunction with git_tag
                or git_commit. The maximum length is 255 characters, e.g.
                `main`.
            - git_tag:
                Name of the tag to be checked out and used by this job. This
                field cannot be specified in conjunction with git_branch or
                git_commit. The maximum length is 255 characters, e.g.
                `release-1.0.0`.
            - git_commit:
                Commit to be checked out and used by this job. This field
                cannot be specified in conjunction with git_branch or
                git_tag. The maximum length is 64 characters, e.g.
                `e0056d01`.
            - git_snapshot:
                Read-only state of the remote repository at the time the job was run.
                            This field is only included on job runs.
        timeout_seconds:
            An optional timeout applied to each run of this job. The default
            behavior is to have no timeout, e.g. `86400`.
        idempotency_token:
            An optional token that can be used to guarantee the idempotency of job
            run requests. If a run with the provided token already
            exists, the request does not create a new run but returns
            the ID of the existing run instead.  If you specify the
            idempotency token, upon failure you can retry until the
            request succeeds. Databricks guarantees that exactly one run
            is launched with that idempotency token.  This token must
            have at most 64 characters.  For more information, see [How
            to ensure idempotency for
            jobs](https://kb.databricks.com/jobs/jobs-idempotency.html),
            e.g. `8f018174-4792-40d5-bcbc-3e6a527352c8`.
        access_control_list:
            List of permissions to set on the job.
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/runs/submit?](
    https://{databricks_instance}/api/2.1/jobs/runs/submit?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Run was created and started successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/runs/submit"  # noqa
    responses = {
        200: "Run was created and started successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    data = {
        "tasks": tasks,
        "run_name": run_name,
        "git_source": git_source,
        "timeout_seconds": timeout_seconds,
        "idempotency_token": idempotency_token,
        "access_control_list": access_control_list,
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
async def get_2_1_jobs_runs_list(
    databricks_instance: str,
    job_id: int,
    run_type: str,
    databricks_credentials: "DatabricksCredentials",
    active_only: bool = False,
    completed_only: bool = False,
    offset: int = 0,
    limit: int = 25,
    expand_tasks: bool = False,
    start_time_from: int = None,
    start_time_to: int = None,
) -> Dict[str, Any]:
    """
    List runs in descending order by start time.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        job_id:
            The job for which to list runs. If omitted, the Jobs service lists runs
            from all jobs.
        run_type:
            The type of runs to return. For a description of run types, see
            [Run](https://docs.databricks.com/dev-
            tools/api/latest/jobs.html
            operation/JobsRunsGet).
        databricks_credentials:
            Credentials to use for authentication with Databricks.
        active_only:
            If active_only is `true`, only active runs are included in the results;
            otherwise, lists both active and completed runs. An active
            run is a run in the `PENDING`, `RUNNING`, or `TERMINATING`.
            This field cannot be `true` when completed_only is `true`.
        completed_only:
            If completed_only is `true`, only completed runs are included in the
            results; otherwise, lists both active and completed runs.
            This field cannot be `true` when active_only is `true`.
        offset:
            The offset of the first run to return, relative to the most recent run.
        limit:
            The number of runs to return. This value must be greater than 0 and less
            than 25\. The default value is 25\. If a request specifies a
            limit of 0, the service instead uses the maximum limit.
        expand_tasks:
            Whether to include task and cluster details in the response.
        start_time_from:
            Show runs that started _at or after_ this value. The value must be a UTC
            timestamp in milliseconds. Can be combined with
            _start_time_to_ to filter by a time range.
        start_time_to:
            Show runs that started _at or before_ this value. The value must be a
            UTC timestamp in milliseconds. Can be combined with
            _start_time_from_ to filter by a time range.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/runs/list?&active_only=%s&completed_only=%s&job_id=%s&offset=%s&limit=%s&run_type=%s&expand_tasks=%s&start_time_from=%s&start_time_to=%s](
    https://{databricks_instance}/api/2.1/jobs/runs/list?&active_only=%s&completed_only=%s&job_id=%s&offset=%s&limit=%s&run_type=%s&expand_tasks=%s&start_time_from=%s&start_time_to=%s)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | List of runs was retrieved successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/runs/list"  # noqa
    responses = {
        200: "List of runs was retrieved successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    params = {
        "active_only": active_only,
        "completed_only": completed_only,
        "job_id": job_id,
        "offset": offset,
        "limit": limit,
        "run_type": run_type,
        "expand_tasks": expand_tasks,
        "start_time_from": start_time_from,
        "start_time_to": start_time_to,
    }

    result = await execute_endpoint.fn(
        url,
        databricks_credentials,
        http_method=HTTPMethod.GET,
        params=params,
        responses=responses,
    )
    return result


@task
async def get_2_1_jobs_runs_get(
    databricks_instance: str,
    run_id: int,
    databricks_credentials: "DatabricksCredentials",
    include_history: bool = None,
) -> Dict[str, Any]:
    """
    Retrieve the metadata of a run.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        run_id:
            The canonical identifier of the run for which to retrieve the metadata.
            This field is required.
        databricks_credentials:
            Credentials to use for authentication with Databricks.
        include_history:
            Whether to include the repair history in the response.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/runs/get?&run_id=%s&include_history=%s](
    https://{databricks_instance}/api/2.1/jobs/runs/get?&run_id=%s&include_history=%s)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Run was retrieved successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/runs/get"  # noqa
    responses = {
        200: "Run was retrieved successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    params = {
        "run_id": run_id,
        "include_history": include_history,
    }

    result = await execute_endpoint.fn(
        url,
        databricks_credentials,
        http_method=HTTPMethod.GET,
        params=params,
        responses=responses,
    )
    return result


@task
async def get_2_0_jobs_runs_export(
    databricks_instance: str,
    run_id: int,
    views_to_export: str,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Export and retrieve the job run task.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        run_id:
            The canonical identifier for the run. This field is required.
        views_to_export:
            Which views to export (CODE, DASHBOARDS, or ALL). Defaults to CODE.
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.0/jobs/runs/export?&run_id=%s&views_to_export=%s](
    https://{databricks_instance}/api/2.0/jobs/runs/export?&run_id=%s&views_to_export=%s)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Run was exported successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.0/jobs/runs/export"  # noqa
    responses = {
        200: "Run was exported successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    params = {
        "run_id": run_id,
        "views_to_export": views_to_export,
    }

    result = await execute_endpoint.fn(
        url,
        databricks_credentials,
        http_method=HTTPMethod.GET,
        params=params,
        responses=responses,
    )
    return result


@task
async def post_2_1_jobs_runs_cancel(
    databricks_instance: str,
    run_id: int,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Cancels a run. The run is canceled asynchronously, so when this request
    completes, the run may still be running. The run are terminated shortly. If
    the run is already in a terminal `life_cycle_state`, this method is a no-op.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        run_id:
            This field is required, e.g. `455644833`.
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/runs/cancel?](
    https://{databricks_instance}/api/2.1/jobs/runs/cancel?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Run was cancelled successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/runs/cancel"  # noqa
    responses = {
        200: "Run was cancelled successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    data = {
        "run_id": run_id,
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
async def get_2_1_jobs_runs_get_output(
    databricks_instance: str,
    run_id: int,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Retrieve the output and metadata of a run. When a notebook task returns a value
    through the dbutils.notebook.exit() call, you can use this endpoint to
    retrieve that value. Databricks restricts this API to return the first 5 MB
    of the output. To return a larger result, you can store job results in a
    cloud storage service. This endpoint validates that the run_id parameter is
    valid and returns an HTTP status code 400 if the run_id parameter is
    invalid. Runs are automatically removed after 60 days. If you to want to
    reference them beyond 60 days, you must save old run results before they
    expire. To export using the UI, see Export job run results. To export using
    the Jobs API, see Runs export.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        run_id:
            The canonical identifier for the run. This field is required.
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/runs/get-output?&run_id=%s](
    https://{databricks_instance}/api/2.1/jobs/runs/get-output?&run_id=%s)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Run output was retrieved successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/runs/get-output"  # noqa
    responses = {
        200: "Run output was retrieved successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    params = {
        "run_id": run_id,
    }

    result = await execute_endpoint.fn(
        url,
        databricks_credentials,
        http_method=HTTPMethod.GET,
        params=params,
        responses=responses,
    )
    return result


@task
async def post_2_1_jobs_runs_delete(
    databricks_instance: str,
    run_id: int,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Deletes a non-active run. Returns an error if the run is active.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        run_id:
            The canonical identifier of the run for which to retrieve the metadata,
            e.g. `455644833`.
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/runs/delete?](
    https://{databricks_instance}/api/2.1/jobs/runs/delete?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Run was deleted successfully. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/runs/delete"  # noqa
    responses = {
        200: "Run was deleted successfully.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    data = {
        "run_id": run_id,
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
async def post_2_1_jobs_runs_repair(
    databricks_instance: str,
    run_id: int,
    rerun_tasks: list,
    latest_repair_id: int,
    jar_params: list,
    notebook_params: dict,
    python_params: list,
    spark_submit_params: list,
    python_named_params: dict,
    databricks_credentials: "DatabricksCredentials",
) -> Dict[str, Any]:
    """
    Re-run one or more tasks. Tasks are re-run as part of the original job run, use
    the current job and task settings, and can be viewed in the history for the
    original job run.

    Args:
        databricks_instance:
            Databricks instance used in formatting the endpoint URL.
        run_id:
            The job run ID of the run to repair. The run must not be in progress,
            e.g. `455644833`.
        rerun_tasks:
            The task keys of the task runs to repair, e.g.
            ```
            ["task0", "task1"]
            ```
        latest_repair_id:
            The ID of the latest repair. This parameter is not required when
            repairing a run for the first time, but must be provided on
            subsequent requests to repair the same run, e.g.
            `734650698524280`.
        jar_params:
            A list of parameters for jobs with Spark JAR tasks, for example
            `"jar_params": ["john doe", "35"]`. The parameters are used
            to invoke the main function of the main class specified in
            the Spark JAR task. If not specified upon `run-now`, it
            defaults to an empty list. jar_params cannot be specified in
            conjunction with notebook_params. The JSON representation of
            this field (for example `{"jar_params":["john doe","35"]}`)
            cannot exceed 10,000 bytes.  Use [Task parameter
            variables](https://docs.databricks.com/jobs.html
            parameter-variables) to set parameters containing
            information about job runs, e.g.
            ```
            ["john", "doe", "35"]
            ```
        notebook_params:
            A map from keys to values for jobs with notebook task, for example
            `"notebook_params": {"name": "john doe", "age": "35"}`. The
            map is passed to the notebook and is accessible through the
            [dbutils.widgets.get](https://docs.databricks.com/dev-
            tools/databricks-utils.html
            dbutils-widgets) function.  If not specified upon `run-now`,
            the triggered run uses the job’s base parameters.
            notebook_params cannot be specified in conjunction with
            jar_params.  Use [Task parameter
            variables](https://docs.databricks.com/jobs.html
            parameter-variables) to set parameters containing
            information about job runs.  The JSON representation of this
            field (for example `{"notebook_params":{"name":"john
            doe","age":"35"}}`) cannot exceed 10,000 bytes, e.g.
            ```
            {"name": "john doe", "age": "35"}
            ```
        python_params:
            A list of parameters for jobs with Python tasks, for example
            `"python_params": ["john doe", "35"]`. The parameters are
            passed to Python file as command-line parameters. If
            specified upon `run-now`, it would overwrite the parameters
            specified in job setting. The JSON representation of this
            field (for example `{"python_params":["john doe","35"]}`)
            cannot exceed 10,000 bytes.  Use [Task parameter
            variables](https://docs.databricks.com/jobs.html
            parameter-variables) to set parameters containing
            information about job runs.  Important  These parameters
            accept only Latin characters (ASCII character set). Using
            non-ASCII characters returns an error. Examples of invalid,
            non-ASCII characters are Chinese, Japanese kanjis, and
            emojis, e.g.
            ```
            ["john doe", "35"]
            ```
        spark_submit_params:
            A list of parameters for jobs with spark submit task, for example
            `"spark_submit_params": ["--class",
            "org.apache.spark.examples.SparkPi"]`. The parameters are
            passed to spark-submit script as command-line parameters. If
            specified upon `run-now`, it would overwrite the parameters
            specified in job setting. The JSON representation of this
            field (for example `{"python_params":["john doe","35"]}`)
            cannot exceed 10,000 bytes.  Use [Task parameter
            variables](https://docs.databricks.com/jobs.html
            parameter-variables) to set parameters containing
            information about job runs.  Important  These parameters
            accept only Latin characters (ASCII character set). Using
            non-ASCII characters returns an error. Examples of invalid,
            non-ASCII characters are Chinese, Japanese kanjis, and
            emojis, e.g.
            ```
            ["--class", "org.apache.spark.examples.SparkPi"]
            ```
        python_named_params:
            A map from keys to values for jobs with Python wheel task, for example
            `"python_named_params": {"name": "task", "data":
            "dbfs:/path/to/data.json"}`, e.g.
            ```
            {"name": "task", "data": "dbfs:/path/to/data.json"}
            ```
        databricks_credentials:
            Credentials to use for authentication with Databricks.

    Returns:
        A dict of the response.

    <h4>API Endpoint URL Format:</h4>
    To format the URL, replace the placeholders, `%s`, with desired values.<br>
    [https://{databricks_instance}/api/2.1/jobs/runs/repair?](
    https://{databricks_instance}/api/2.1/jobs/runs/repair?)

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Run repair was initiated. |
    | 400 | The request was malformed. See JSON response for error details. |
    | 401 | The request was unauthorized. |
    | 500 | The request was not handled correctly due to a server error. |
    """  # noqa
    url = f"https://{databricks_instance}/api/2.1/jobs/runs/repair"  # noqa
    responses = {
        200: "Run repair was initiated.",  # noqa
        400: "The request was malformed. See JSON response for error details.",  # noqa
        401: "The request was unauthorized.",  # noqa
        500: "The request was not handled correctly due to a server error.",  # noqa
    }

    data = {
        "run_id": run_id,
        "rerun_tasks": rerun_tasks,
        "latest_repair_id": latest_repair_id,
        "jar_params": jar_params,
        "notebook_params": notebook_params,
        "python_params": python_params,
        "spark_submit_params": spark_submit_params,
        "python_named_params": python_named_params,
    }

    result = await execute_endpoint.fn(
        url,
        databricks_credentials,
        http_method=HTTPMethod.POST,
        responses=responses,
        data=data,
    )
    return result
