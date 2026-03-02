
from dagster import AssetExecutionContext, AssetKey, AutoMaterializePolicy
from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator
import os
import json
from pathlib import Path

# Use path relative to this file to be robust
DBT_PROJECT_DIR = Path(__file__).joinpath("..", "..", "..", "..", "dbt_project").resolve()

class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props):
        resource_type = dbt_resource_props["resource_type"]
        name = dbt_resource_props["name"]
        
        # Map dbt source 'retail_source.raw_orders' to asset 'raw_orders'
        if resource_type == "source":
            return AssetKey(name)
            
        return super().get_asset_key(dbt_resource_props)
        
    def get_auto_materialize_policy(self, dbt_resource_props):
        # Enable auto-materialization for all dbt models
        return AutoMaterializePolicy.eager()
        
    def get_group_name(self, dbt_resource_props):
        # Group assets based on their directory structure
        fqn = dbt_resource_props.get("fqn", [])
        if "staging" in fqn:
            return "staging"
        if "marts" in fqn:
            return "marts"
        return "default"

@dbt_assets(
    manifest=os.path.join(DBT_PROJECT_DIR, "target", "manifest.json"),
    dagster_dbt_translator=CustomDagsterDbtTranslator()
)
def retail_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
