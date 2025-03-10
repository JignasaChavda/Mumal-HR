import frappe

def execute(filters=None):
    # Define columns for the report
    columns = [
        {"label": "UAN", "fieldname": "uan_number", "fieldtype": "Data"},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data"},
        {"label": "GROSS WAGES", "fieldname": "gross_pay", "fieldtype": "Data"},
        {"label": "EPF WAGES", "fieldname": "epf_wages", "fieldtype": "Data"},
        {"label": "EPS WAGES", "fieldname": "eps_wages", "fieldtype": "Data"},
        {"label": "EDLI WAGES", "fieldname": "edli_wages", "fieldtype": "Data"},
        {"label": "EE SHARE REMITTED", "fieldname": "ee_share_remitted", "fieldtype": "Data"},
        {"label": "EPS CONTRIBUTION REMITTED", "fieldname": "eps_contribution_remitted", "fieldtype": "Data"},
        {"label": "ER SHARE REMITTED", "fieldname": "er_share_remitted", "fieldtype": "Data"},
        {"label": "NCP DAYS", "fieldname": "leave_without_pay", "fieldtype": "Data"},
        {"label": "REFUNDS", "fieldname": "refunds", "fieldtype": "Data"}
    ]

    # Base SQL query
    sql_query = """
        SELECT DISTINCT
            e.uan_number,
            e.employee_name,
            s.name AS salary_slip,
            s.gross_pay,
            s.leave_without_pay
        FROM `tabSalary Slip` s
        LEFT JOIN `tabEmployee` e ON s.employee = e.name
        WHERE e.custom_pf = 1
    """

    # Prepare the condition for filtering
    condition = ""
    params = {}

    if filters:
        company = filters.get("company")
        from_date = filters.get("from_date")
        to_date = filters.get("to_date")

        if company:
            condition += " AND e.company = %(company)s"
            params["company"] = company

        if from_date and to_date:
            condition += " AND s.start_date >= %(from_date)s AND s.end_date <= %(to_date)s"
            params["from_date"] = from_date
            params["to_date"] = to_date

    # Final SQL Query
    final_query = sql_query + condition

    # Execute SQL query
    salary_slips = frappe.db.sql(final_query, params, as_dict=True)
    data = []

    for slip in salary_slips:
        # Fetch House Rent Allowance from Earnings table
        hra_amount = frappe.db.get_value(
            "Salary Detail",
            {"parent": slip["salary_slip"], "abbr": "HRA"},  # Ensure "HRA" is the correct abbreviation
            "amount"
        ) or 0

        # Calculate EPF Wages
        gross_wages = round(slip["gross_pay"] - hra_amount)
        epf_wages = min(gross_wages, 15000)

        # Set EPS Wages and EDLI Wages same as EPF Wages
        eps_wages = epf_wages
        edli_wages = epf_wages
        ee_share_remitted = round(epf_wages * 0.12)
        eps_contribution_remitted = round(eps_wages * 0.0833)
        er_share_remitted = ee_share_remitted - eps_contribution_remitted

        data.append({
            "uan_number": slip["uan_number"],
            "employee_name": slip["employee_name"],
            "gross_pay": gross_wages,
            "epf_wages": epf_wages,
            "eps_wages": eps_wages,
            "edli_wages": edli_wages,
            "ee_share_remitted": ee_share_remitted,
            "eps_contribution_remitted": eps_contribution_remitted,
            "er_share_remitted": er_share_remitted
        })

    return columns, data
