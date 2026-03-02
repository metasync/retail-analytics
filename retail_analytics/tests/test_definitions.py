
from retail_analytics.definitions import defs

def test_definitions_load():
    """
    Smoke test to ensure that the Dagster definitions can be loaded without error.
    This catches syntax errors, import errors, and invalid resource configurations.
    """
    assert defs
    assert len(defs.assets) > 0
    assert "starrocks" in defs.resources
    assert "dbt" in defs.resources
