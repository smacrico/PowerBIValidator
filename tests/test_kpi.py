def test_kpi_validation():

    python_kpis = calculate_kpis(df)
    powerbi_kpis = get_powerbi_results()

    for kpi in python_kpis:

        assert python_kpis[kpi] == powerbi_kpis[kpi]

# This allows automated checks in:

# GitHub Actions

# Azure DevOps

# Jenkins


from src.kpi_calculator import calculate_kpis

def test_kpi_calculation(sample_df):

    kpis = calculate_kpis(sample_df)

    assert kpis["TotalActions"] >= 0