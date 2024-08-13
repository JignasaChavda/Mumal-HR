
import frappe
from frappe import _


@frappe.whitelist()
def get_employee_details(employee):
    employee_doc = frappe.get_doc('Employee', employee)
    father_name = ""
    
    if employee_doc.middle_name and employee_doc.last_name:
        # Merge middle_name and last_name into full_name
        father_name = " ".join([employee_doc.middle_name, employee_doc.last_name])
    else:
        father_name = ""

    return {
        'employee_name': employee_doc.employee_name,
        'employee_id': employee_doc.name,
        'middle_name': employee_doc.middle_name,
        'last_name': employee_doc.last_name,
        'employee_name': employee_doc.employee_name,
        'department': employee_doc.department,
        'date_of_joining': employee_doc.date_of_joining,
        'father_name': father_name
    }

