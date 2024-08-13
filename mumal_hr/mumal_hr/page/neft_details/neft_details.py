import frappe
from frappe.utils import nowdate, get_first_day, get_last_day, formatdate, money_in_words

@frappe.whitelist()
def get_all_company_data(from_date, to_date,  employee_name=None):
    companies = frappe.get_all('Company', fields=['*'])
    return {
        'from_date': from_date,
        'to_date': to_date,
        'employee_name': employee_name
    }


@frappe.whitelist()
def default_field_value():
    user_default_company = frappe.defaults.get_user_default('Company')
    start_date = get_first_day(nowdate())
    end_date = get_last_day(nowdate())
    return start_date, end_date, user_default_company

@frappe.whitelist()
def get_attendance_data(from_date=None, to_date=None, company_name=None, employee_name=None):
    conditions = []
    values = []
    
    if company_name:
        conditions.append("company = %s")
        values.append(company_name)
        
    if employee_name:
        conditions.append("employee = %s")
        values.append(employee_name)
    
    if from_date and to_date:
        conditions.append("(start_date BETWEEN %s AND %s AND end_date BETWEEN %s AND %s)")
        values.extend([from_date, to_date, from_date, to_date])
    
    condition_str = " AND ".join(conditions)
    
    # Fetch all Salary Slip records matching the conditions
    query = f"""
        SELECT name, employee, start_date, department, company, employee_name, bank_account_no, net_pay, total_in_words
        FROM `tabSalary Slip`
        WHERE {condition_str}
    """
    
    attendance_data = frappe.db.sql(query, tuple(values), as_dict=True)
    
    for record in attendance_data:
        record["total_in_words"] = money_in_words(record["net_pay"])
    
    return attendance_data



@frappe.whitelist()
def convert_to_words(amount):
    return money_in_words(amount)

@frappe.whitelist()
def get_company_address(company_name):
    query = """
        SELECT ad.address_line1, ad.address_line2, ad.city, ad.state, ad.pincode, ad.country, ad.phone, ad.fax, ad.email_id
        FROM `tabAddress` AS ad
        JOIN `tabDynamic Link` AS dl ON dl.parent = ad.name
        WHERE dl.link_doctype = 'Company' AND dl.link_name = %s
        ORDER BY ad.creation ASC
        LIMIT 1
    """
    address = frappe.db.sql(query, company_name, as_dict=True)

    if address:
        return {'address': address[0]}
    else:
        return {'address': None}
