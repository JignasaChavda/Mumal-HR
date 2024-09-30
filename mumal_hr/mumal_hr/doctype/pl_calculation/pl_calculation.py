# Copyright (c) 2024, jignasha@sanskartechnolab.com and contributors
# For license information, please see license.txt


import frappe
from dateutil.relativedelta import relativedelta
from frappe.model.document import Document
from calendar import calendar, monthrange
from datetime import datetime, timedelta




class PLCalculation(Document):
    def on_submit(self):
        # Fetch current active leave period
        leave_period = frappe.db.get_value("Leave Period", 
            filters={
                "is_active": 1,
                "from_date": ['<=', self.from_date],
                "to_date": ['>=', self.to_date]
            }, 
            fieldname='name'
        )

        # Check if leave_period is found
        if leave_period:
            frappe.msgprint(f"Leave Period found: {leave_period}")
        else:
            frappe.throw("No active leave period found for the selected dates.")

        cur_doc = frappe.get_doc("PL Calculation", self.name)
        emp_details = cur_doc.get("encashment_details")

        for emp in emp_details:
            if emp.eligible_leave != 0 and emp.carry_forward == 1:
                
                # Generate current year leave allocation
                new_allocation = frappe.get_doc({
                    "doctype": "Leave Allocation", 
                    "employee": emp.employee,
                    "employee_name": emp.employee_name,
                    "leave_type": self.leave_type,
                    "from_date": self.from_date,
                    "to_date": self.to_date,
                    "new_leaves_allocated": emp.eligible_leave,
                    "total_leaves_allocated": emp.eligible_leave,
                    "custom_pl_calculation": self.name
                })
                
                # Insert and submit leave allocation
                new_allocation.insert(ignore_permissions=True, ignore_mandatory=True)
                new_allocation.submit()
                
                # Store the leave allocation name for encashment reference
                past_allocation = new_allocation.name
                frappe.msgprint(f"Leave Allocation {past_allocation} created for Employee {emp.employee}")

            
                new_allocation = frappe.new_doc("Leave Allocation")
                new_allocation.employee = emp.employee
                new_allocation.employee_name = emp.employee_name
                new_allocation.leave_type = self.leave_type
                new_allocation.from_date = self.next_year_start_date
                new_allocation.to_date = self.next_year_end_date
                new_allocation.carry_forward = 1
            
                new_allocation.insert(ignore_permissions=True)
                new_allocation.submit()






@frappe.whitelist()
def get_encashment_details(from_date, to_date, leave_type):
    employees = frappe.get_all('Employee', 
        filters={'status': 'Active'},
        fields=['employee', 'employee_name', 'department', 'designation', 'custom_payroll_category', 'custom_gross_salary_per_month', 'custom_daily_rate', 'custom_standard_working_days'])

    result = {}

    leave_doc = frappe.get_doc('Leave Type', leave_type)
    one_leave_per_month = leave_doc.get("custom_1_leave_per_days")

    for employee in employees:
        employee_dict = result.get(employee.employee, {
            'employee': employee.employee,
            'employee_name': employee.employee_name,
            'department': employee.department,
            'designation': employee.designation,
            'payroll_category': employee.custom_payroll_category,
            'monthly_attendance': [],  # Store monthly attendance here
            'present_days': 0,  # Total attendance count for all months
            'eligible_leaves': 0  # Total eligible leaves for all months
        })

        attendance_records = frappe.get_all('Attendance', 
                filters={
                    'employee': employee.employee,
                    'attendance_date': ['between', [from_date, to_date]],
                    'status': ['in', ['Present', 'Half Day']]
                },
                fields=['status']
            )

        attendance_count = sum(1 if record.status == 'Present' else 0.5 for record in attendance_records)

        if attendance_count >= 20:
            eligible_leaves = attendance_count / one_leave_per_month
        else:
            eligible_leaves = 0

        employee_dict['present_days'] = attendance_count
        if eligible_leaves:
            
            decimal_part = str(eligible_leaves).split('.')
            if len(decimal_part) > 1 and decimal_part[1]: 
                first_digit_after_decimal = int(decimal_part[1][0])  
                if first_digit_after_decimal < 5:
                    final_leave = int(decimal_part[0]) + 0.5  
                    employee_dict['eligible_leaves'] = final_leave
                else:
                    final_leave = int(decimal_part[0]) + 1  
                    employee_dict['eligible_leaves'] = final_leave
                

        if employee.custom_payroll_category == 'Monthly':
            employee_dict['gross_salary'] = employee.custom_gross_salary_per_month
            if employee.custom_gross_salary_per_month and employee.custom_standard_working_days:
                employee_dict['salary_per_day'] = employee.custom_gross_salary_per_month / employee.custom_standard_working_days
                employee_dict['amount'] = employee_dict['salary_per_day'] * eligible_leaves
        elif employee.custom_payroll_category == 'Daily':
            if employee.custom_daily_rate:
                employee_dict['daily_rate'] = employee.custom_daily_rate
                employee_dict['amount'] = employee_dict['daily_rate'] * eligible_leaves

        result[employee.employee] = employee_dict

    return result

