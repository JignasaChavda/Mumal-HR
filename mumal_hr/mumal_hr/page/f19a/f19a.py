from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def get_all_company_data(company_name=None, employee_name=None, department=None):
    conditions = []
    values = {}

    if company_name:
        conditions.append("company = %(company)s")
        values["company"] = company_name

    if employee_name:
        conditions.append("name = %(employee_name)s")
        values["employee_name"] = employee_name

    if department:
        conditions.append("department = %(department)s")
        values["department"] = department

    condition_str = " AND ".join(conditions) if conditions else "1=1"

    employee_data = frappe.db.sql("""
        SELECT name, employee_name, current_address, department
        FROM `tabEmployee`
        WHERE {condition_str}
    """.format(condition_str=condition_str), values, as_dict=True)

    return {
        'employee_data': employee_data
    }

@frappe.whitelist()
def get_default_company():
    user_default_company = frappe.defaults.get_user_default('Company')
    return user_default_company

@frappe.whitelist()
def get_employee_data(company_name=None, employee_name=None, department=None):
    conditions = []
    values = []

    if company_name:
        conditions.append("company = %s")
        values.append(company_name)

    if employee_name:
        conditions.append("name = %s")
        values.append(employee_name)

    if department:
        conditions.append("department = %s")
        values.append(department)

    condition_str = " AND ".join(conditions) if conditions else "1=1"

    employee_data = frappe.db.sql(f"""
        SELECT name, employee_name, current_address, department
        FROM `tabEmployee`
        WHERE {condition_str}
    """, tuple(values), as_dict=True)

    return employee_data

