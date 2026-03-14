import re


def translate_dax(dax):

    dax = dax.strip().upper()

    if "COUNTROWS" in dax:
        return "len(df)"

    if "DISTINCTCOUNT" in dax:

        column = re.findall(r"\((.*?)\)", dax)[0]

        return f'df["{column}"].nunique()'

    if "DIVIDE" in dax:

        return "numerator / denominator"

    if "SUM(" in dax:

        column = re.findall(r"\((.*?)\)", dax)[0]

        return f'df["{column}"].sum()'

    return "Unsupported DAX expression"
