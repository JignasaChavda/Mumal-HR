import frappe
from hrms.hr.utils import get_holiday_dates_for_employee, validate_active_employee
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip as OriginalSalarySlip


class SalarySlip(OriginalSalarySlip):
    def calculate_component_amounts(self, component_type):
        if self.is_new():
            if not getattr(self, "_salary_structure_doc", None):
                self._salary_structure_doc = frappe.get_doc("Salary Structure", self.salary_structure)

            self.add_structure_components(component_type)
            self.add_additional_salary_components(component_type)
            if component_type == "earnings":
                self.add_employee_benefits()
            else:
                self.add_tax_components()

    def validate(self):
        self.status = self.get_status()
        validate_active_employee(self.employee)
        self.validate_dates()
        self.check_existing()

        if not self.salary_slip_based_on_timesheet:
            self.get_date_details()

        if not (len(self.get("earnings")) or len(self.get("deductions"))):
            self.get_emp_and_working_day_details()
        else:
            self.get_working_days_details(lwp=self.leave_without_pay)

        self.calculate_custom_working_days()
        self.calculate_net_pay()
        self.compute_year_to_date()
        self.compute_month_to_date()
        self.compute_component_wise_year_to_date()
        self.add_leave_balances()
        self.compute_income_tax_breakup()

        if frappe.db.get_single_value("Payroll Settings", "max_working_hours_against_timesheet"):
            max_working_hours = frappe.db.get_single_value(
                "Payroll Settings", "max_working_hours_against_timesheet"
            )
            if self.salary_slip_based_on_timesheet and (self.total_working_hours > int(max_working_hours)):
                frappe.msgprint(
                    _("Total working hours should not be greater than max working hours {0}").format(
                        max_working_hours
                    ),
                    alert=True,
                )

    def calculate_custom_working_days(self):
        emp = self.employee
        holiday_list = frappe.db.get_value('Employee', emp, 'holiday_list')
        category = frappe.db.get_value('Employee', emp, 'custom_payroll_category')


        payroll_based_on = frappe.db.get_single_value('Payroll Settings', 'payroll_based_on')

        general_holidays = frappe.get_all('Holiday', {
            'parent': holiday_list,
            'weekly_off': 0,
            'holiday_date': ['between', [self.start_date, self.end_date]]
        }, ['name'])

        holiday_count = len(general_holidays)


        weekly_off = frappe.get_all('Holiday', {
            'parent': holiday_list,
            'weekly_off': 1,
            'holiday_date': ['between', [self.start_date, self.end_date]]
        }, ['name'])

        weekoff_count = len(weekly_off)

        self.custom_general_holidays = holiday_count
        self.custom_week_off = weekoff_count

        new_payment_days = 0
        if category == 'Daily':
            total_days = frappe.utils.date_diff(self.end_date, self.start_date)
            new_working_days = total_days - weekoff_count + 1

            if payroll_based_on == "Leave":
                new_payment_days = new_working_days - self.leave_without_pay
            elif payroll_based_on == "Attendance":
                new_payment_days = new_working_days - self.absent_days

            self.total_working_days = new_working_days
            self.payment_days = new_payment_days
