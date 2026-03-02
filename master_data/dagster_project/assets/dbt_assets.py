import os
from pathlib import Path

from dagster import AssetExecutionContext, AssetKey, AssetSelection, define_asset_job
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject

# Identify the dbt project path
dbt_project_dir = Path(__file__).joinpath("..", "..", "..", "dbt_project").resolve()
dbt_project = DbtProject(project_dir=dbt_project_dir)

@dbt_assets(manifest=dbt_project.manifest_path)
def master_data_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
