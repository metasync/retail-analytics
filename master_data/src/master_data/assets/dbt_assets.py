
import os
from pathlib import Path

from dagster import AssetExecutionContext, AssetKey, AssetSelection, define_asset_job, AutoMaterializePolicy
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject, DagsterDbtTranslator

# Identify the dbt project path
dbt_project_dir = Path(__file__).joinpath("..", "..", "..", "..", "dbt_project").resolve()
dbt_project = DbtProject(project_dir=dbt_project_dir)

class CustomMasterDataDbtTranslator(DagsterDbtTranslator):
    def get_auto_materialize_policy(self, dbt_resource_props):
        # Enable auto-materialization for all dbt models
        return AutoMaterializePolicy.eager()
        
    def get_group_name(self, dbt_resource_props):
        return "master"

@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=CustomMasterDataDbtTranslator()
)
def master_data_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
