from kpi_calculator import calculate_kpis
from validator import validate
from dashboards import get_powerbi_results  

def test_kpi_validation():

    python_kpis = calculate_kpis(df)
    powerbi_kpis = get_powerbi_results()

    for kpi in python_kpis:

        assert python_kpis[kpi] == powerbi_kpis[kpi]