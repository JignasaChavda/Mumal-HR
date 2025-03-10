import frappe

def execute(filters=None):
    # Define columns for the report
    columns = [
        {"label": "IP Number", "fieldname": "esi_number", "fieldtype": "Data"},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data"},
        {"label": "Days Worked", "fieldname": "payment_days", "fieldtype": "Data"},
        {"label": "GROSS WAGES", "fieldname": "gross_pay", "fieldtype": "Data"},
        {"label": "Reason Code", "fieldname": "reason_code", "fieldtype": "Data"},
        {"label": "Last Working Day", "fieldname": "relieving_date", "fieldtype": "Data"},
    ]
    
    # Base SQL query
    sql_query = """
        SELECT 
            e.esi_number, 
            e.employee_name, 
            s.payment_days, 
            s.gross_pay, 
            CASE 
                WHEN s.leave_without_pay > 0 THEN '1' 
                WHEN e.status = 'Left' AND e.relieving_date BETWEEN s.start_date AND s.end_date THEN '2' 
                WHEN e.date_of_retirement BETWEEN s.start_date AND s.end_date THEN '3' 
                ELSE '0'  -- Default to '0' when no other reason applies
            END AS reason_code, 
            CASE 
                WHEN e.status = 'Left' AND e.relieving_date BETWEEN s.start_date AND s.end_date THEN DATE_FORMAT(e.relieving_date, '%%d-%%m-%%Y')
                WHEN e.date_of_retirement BETWEEN s.start_date AND s.end_date THEN DATE_FORMAT(e.date_of_retirement, '%%d-%%m-%%Y')
                ELSE ''
            END AS relieving_date
        FROM `tabSalary Slip` s
        LEFT JOIN `tabEmployee` e ON s.employee = e.name
        WHERE s.docstatus = 1
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
