import frappe

def execute(filters=None):
    columns, data = [], []

    columns = [
        {
            "label": "EMP ID",
            "fieldname": "employee",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Employee Name",
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Department",
            "fieldname": "department",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": "Designation",
            "fieldname": "designation",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Date of Joining",
            "fieldname": "date_of_joining",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": "Current Gross Salary",
            "fieldname": "current_gross_salary",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": "Applicable From",
            "fieldname": "applicable_from",
            "fieldtype": "Date",
            "width": 130,
        },
        {
            "label": "Increment Amount",
            "fieldname": "increment_amount",
            "fieldtype": "Float",
            "width": 140,
        },
        {
            "label": "Increment (%)",
            "fieldname": "increment_percentage",
            "fieldtype": "Float",
            "width": 120,
        },
        {
            "label": "Proposed Increment (%) as per Matrix",
            "fieldname": "proposed_increment_percentage_matrix",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Proposed Increment As per Matrix",
            "fieldname": "proposed_increment_matrix",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Approved by Management",
            "fieldname": "approved_by_management",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Proposed Designation",
            "fieldname": "proposed_designation",
            "fieldtype": "Data",
            "width": 150,
        },
    ]

    sql = """
        SELECT
            ei.employee AS employee,
            ei.employee_name AS employee_name,
            ei.department AS department,
            emp.designation AS designation,
            emp.date_of_joining AS date_of_joining,
            emp.custom_gross_salary_per_month AS current_gross_salary,
            ei.applicable_from AS applicable_from,
            ei.increment_amount AS increment_amount,
            ei.increment_percentage AS increment_percentage
        FROM
            `tabEmployee Increment` ei
        JOIN
            `tabEmployee` emp ON emp.name = ei.employee
        WHERE
            ei.docstatus = 1
    """

    conditions = []
    sql_args = []

    if filters:
        if filters.get("employee"):
            conditions.append("ei.employee = %s")
            sql_args.append(filters.get("employee"))

        if filters.get("from_date"):
            conditions.append("ei.applicable_from >= %s")
            sql_args.append(filters.get("from_date"))

        if filters.get("to_date"):
            conditions.append("ei.applicable_from <= %s")
            sql_args.append(filters.get("to_date"))

    if conditions:
        sql += " AND " + " AND ".join(conditions)

    sql += " ORDER BY ei.employee, ei.applicable_from DESC"

    data = frappe.db.sql(sql, tuple(sql_args), as_dict=True)

    return columns, data
