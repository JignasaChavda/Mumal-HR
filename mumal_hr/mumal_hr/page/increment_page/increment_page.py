from frappe.utils import nowdate, get_first_day, get_last_day
import frappe

@frappe.whitelist()
def get_all_company_data(company_name=None, employee_name=None):
    companies = frappe.get_all('Company', fields=['*'])
    return {
        'company': companies,
        'employee_name': employee_name
    }

@frappe.whitelist()
def get_default_company():
    user_default_company = frappe.defaults.get_user_default('Company')
    return user_default_company




@frappe.whitelist()
def get_employee_data(company_name=None, employee_name=None):
    conditions = []
    values = []

    if company_name:
        conditions.append("company = %s")
        values.append(company_name)

    if employee_name:
        conditions.append("name = %s")
        values.append(employee_name)    

    condition_str = " AND ".join(conditions) if conditions else "1=1"

    # employee_data = frappe.db.sql(f"""
    #     SELECT name, employee_name, current_address, department, designation, date_of_joining
    #     FROM `tabEmployee`
    #     WHERE {condition_str}
    # """, tuple(values), as_dict=True)
    employee_data = frappe.db.sql(f"""
        SELECT e.name, e.employee_name, e.current_address, e.department, e.designation, e.date_of_joining,
            GROUP_CONCAT(edu.qualification SEPARATOR ', ') as qualifications
        FROM `tabEmployee` e
        LEFT JOIN `tabEmployee Education` edu ON e.name = edu.parent
        WHERE {" AND ".join(conditions).replace('name', 'e.name')}
        GROUP BY e.name
    """, tuple(values), as_dict=True)



    return employee_data

