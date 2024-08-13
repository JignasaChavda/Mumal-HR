import frappe

@frappe.whitelist()
def get_employee_details():
    # Fetch employee details
    employees = frappe.get_all('Employee', fields=['name', 'employee_name', 'designation'])
    return {'employees': employees}
