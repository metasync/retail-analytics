
from dagster_dbt import DbtCliResource
from dagster import Definitions, load_assets_from_modules, EnvVar, DefaultSensorStatus, define_asset_job, ScheduleDefinition, DefaultScheduleStatus
import os
import sys

from dagster_project.assets import source_assets, dbt_assets
from dagster_project.resources.starrocks import StarRocksResource

# Load assets
source_assets_list = load_assets_from_modules([source_assets])
dbt_assets_list = load_assets_from_modules([dbt_assets]) # Requires manifest.json

# Resources
starrocks_resource = StarRocksResource(
    host=EnvVar("STARROCKS_HOST"),
    port=EnvVar.int("STARROCKS_PORT"),
    username=EnvVar("STARROCKS_USER"),
    password=EnvVar("STARROCKS_PASSWORD"),
    database=EnvVar("STARROCKS_DB")
)

dbt_resource = DbtCliResource(
    project_dir=os.getenv("DBT_PROJECT_DIR", "./dbt_project"),
    profiles_dir=os.getenv("DBT_PROFILES_DIR", "./dbt_project"),
    target=os.getenv("DBT_TARGET", "development"),
    dbt_executable=os.path.join(os.path.dirname(sys.executable), "dbt")
)

# Enable the automation condition sensor by default
from dagster import AutomationConditionSensorDefinition
automation_sensor = AutomationConditionSensorDefinition(
    "default_automation_condition_sensor",
    target=source_assets_list + dbt_assets_list,
    default_status=DefaultSensorStatus.RUNNING
)

# Job to check sources for new data
check_sources_job = define_asset_job(
    name="check_sources_job",
    selection=source_assets_list
)

# Schedule to check sources every minute
check_sources_schedule = ScheduleDefinition(
    job=check_sources_job,
    cron_schedule="* * * * *",
    default_status=DefaultScheduleStatus.RUNNING
)

defs = Definitions(
    assets=source_assets_list + dbt_assets_list,
    resources={
        "starrocks": starrocks_resource,
        "dbt": dbt_resource,
    },
    sensors=[automation_sensor],
    jobs=[check_sources_job],
    schedules=[check_sources_schedule]
)
