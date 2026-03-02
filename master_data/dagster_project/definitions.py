import os
import sys
from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource

# Add the project root (master_data) to sys.path to ensure 'dagster_project' package is importable
# This fixes "attempted relative import" and "module not found" errors when loaded via workspace.yaml
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from dagster_project.assets import dbt_assets

dbt_project_dir = dbt_assets.dbt_project.project_dir

defs = Definitions(
    assets=load_assets_from_modules([dbt_assets]),
    resources={
        "dbt": DbtCliResource(project_dir=dbt_project_dir),
    },
)
