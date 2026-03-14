def test_unique_users():

    python_value = df["UPN"].nunique()

    powerbi_value = run_measure("Unique Users")

    assert python_value == powerbi_value