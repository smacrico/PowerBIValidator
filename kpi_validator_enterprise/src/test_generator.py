def generate_test(measure, python_logic):

    return f"""
def test_{measure.lower().replace(' ','_')}():

    python_value = {python_logic}

    powerbi_value = run_measure("{measure}")

    assert python_value == powerbi_value
"""