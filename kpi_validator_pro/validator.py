def validate(python_kpis, powerbi_kpis):

    results = []

    for kpi in python_kpis.keys():

        results.append({
            "Metric": kpi,
            "Python": python_kpis[kpi],
            "PowerBI": powerbi_kpis[kpi],
            "Match": python_kpis[kpi] == powerbi_kpis[kpi]
        })

    return results