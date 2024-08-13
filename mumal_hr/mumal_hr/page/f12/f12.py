# Get Data with company filter
import frappe

@frappe.whitelist()
def get_all_company_data(company_name):
    companies = frappe.get_all('Company', filters={'name': company_name}, fields=['*'])  # Fetch all fields for the selected company
    return companies


@frappe.whitelist()
def get_default_company():
    user_default_company = frappe.defaults.get_user_default('Company')
    return user_default_company


#Get default template
# import frappe

# @frappe.whitelist()
# def get_all_company_data():
#     companies = frappe.get_all('Company', fields=['*'])  # Fetch all fields
#     return companies

