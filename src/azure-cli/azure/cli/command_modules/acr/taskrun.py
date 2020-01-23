# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ._stream_utils import stream_logs
from ._utils import (
    user_confirmation,
    validate_managed_registry
)


TASKRUN_NOT_SUPPORTED = 'TaskRun is only supported for managed registries.'


def acr_taskrun_show(cmd,
                     client,
                     taskrun_name,
                     registry_name,
                     resource_group_name=None):
    _, resource_group_name = validate_managed_registry(
        cmd, registry_name, resource_group_name, TASKRUN_NOT_SUPPORTED)
    return client.get(resource_group_name, registry_name, taskrun_name)


def acr_taskrun_list(cmd,
                     client,
                     registry_name,
                     resource_group_name=None):

    _, resource_group_name = validate_managed_registry(
        cmd, registry_name, resource_group_name, TASKRUN_NOT_SUPPORTED)
    return client.list(resource_group_name, registry_name)


def acr_taskrun_delete(cmd,
                       client,
                       taskrun_name,
                       registry_name,
                       resource_group_name=None,
                       yes=False):
    _, resource_group_name = validate_managed_registry(
        cmd, registry_name, resource_group_name, TASKRUN_NOT_SUPPORTED)

    user_confirmation("Are you sure you want to delete the taskrun '{}' ".format(taskrun_name), yes)
    return client.delete(resource_group_name, registry_name, taskrun_name)


def acr_taskrun_logs(cmd,
                     client,  # cf_acr_runs
                     registry_name,
                     taskrun_name,
                     resource_group_name=None):
    _, resource_group_name = validate_managed_registry(
        cmd, registry_name, resource_group_name, TASKRUN_NOT_SUPPORTED)

    from ._client_factory import cf_acr_taskruns
    client_taskruns = cf_acr_taskruns(cmd.cli_ctx)
    response = acr_taskrun_show(cmd, client_taskruns, taskrun_name, registry_name)
    run_id = response.run_result.run_id

    return stream_logs(client, run_id, registry_name, resource_group_name)
