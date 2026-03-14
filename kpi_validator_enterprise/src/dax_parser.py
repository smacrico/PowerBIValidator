def detect_measure_type(dax):

    dax = dax.upper()

    if "DISTINCTCOUNT" in dax:
        return "distinctcount"

    if "COUNTROWS" in dax:
        return "countrows"

    return "unknown"