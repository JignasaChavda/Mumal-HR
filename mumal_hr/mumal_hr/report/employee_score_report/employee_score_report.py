import frappe

def execute(filters=None):
    # Define columns for the report
    columns = [
        {"label": "Employee ID", "fieldname": "employee", "fieldtype": "Link", "options": "Employee"},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data"},
        {"label": "Department", "fieldname": "department", "fieldtype": "Link", "options": "Department"},
        {"label": "Designation", "fieldname": "designation", "fieldtype": "Link", "options": "Designation"},
        {"label": "Mobile No", "fieldname": "mobile_no", "fieldtype": "Data"}
    ]

    # Initialize data as an empty list
    data = []

    # Base SQL query
    sql_query = """
        SELECT DISTINCT
            s.employee,
            s.employee_name,
            e.department,
            e.designation,
            e.cell_number AS mobile_no
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
    data = frappe.db.sql(final_query, params, as_dict=True)

    return columns, data
