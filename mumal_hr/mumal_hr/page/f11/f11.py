# Python code
import frappe
from frappe.utils import nowdate, get_first_day, get_last_day

@frappe.whitelist()
def get_all_company_data(from_date, to_date, employee_name=None):
    companies = frappe.get_all('Company', fields=['*'])  # Fetch all fields for the selected company
    return {
        'from_date': from_date,
        'to_date': to_date,
        'employee_name': employee_name  # Pass the employee name to the client
    }

@frappe.whitelist()
def default_field_value():
    user_default_company = frappe.defaults.get_user_default('Company')    
    # Get the first day of the current month
    start_date = get_first_day(nowdate())
    end_date = get_last_day(nowdate())

    return start_date, end_date, user_default_company

@frappe.whitelist()
def get_attendance_data(from_date, to_date, company_name=None, employee_name=None):
    # Query attendance records from the Attendance doctype for all employees
    conditions = []
    values = []

    if company_name:
        conditions.append("company = %s")
        values.append(company_name)

    if employee_name:
        conditions.append("employee = %s")
        values.append(employee_name)

    conditions.append("attendance_date BETWEEN %s AND %s")
    values.extend([from_date, to_date])

    condition_str = " AND ".join(conditions)

    attendance_data = frappe.db.sql(f"""
        SELECT employee, attendance_date, department, company, employee_name
        FROM `tabAttendance`
        WHERE {condition_str}
    """, tuple(values), as_dict=True)

    return attendance_data
