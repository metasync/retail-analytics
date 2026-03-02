
import os
import sys
from dagster import Definitions, load_assets_from_modules, DefaultSensorStatus, AutomationConditionSensorDefinition
from dagster_dbt import DbtCliResource

from master_data.assets import dbt_assets

dbt_project_dir = dbt_assets.dbt_project_dir

# Enable automation condition sensor
automation_sensor = AutomationConditionSensorDefinition(
    "master_data_automation_sensor",
    target=load_assets_from_modules([dbt_assets]),
    default_status=DefaultSensorStatus.RUNNING
)

defs = Definitions(
    assets=load_assets_from_modules([dbt_assets]),
    resources={
        "dbt": DbtCliResource(
            project_dir=str(dbt_project_dir),
            profiles_dir=str(dbt_project_dir),
            dbt_executable=os.path.join(os.path.dirname(sys.executable), "dbt")
        ),
    },
    sensors=[automation_sensor]
)
