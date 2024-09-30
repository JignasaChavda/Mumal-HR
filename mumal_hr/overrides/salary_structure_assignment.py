import frappe
from frappe.model.document import Document
import ast
import re

from hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment import SalaryStructureAssignment as Document

def eval_salary_formula(formula, variables):
    try:
        safe_namespace = {"__builtins__": None}
        safe_namespace.update(variables)
        return eval(formula, {"__builtins__": None}, safe_namespace)
    except Exception as e:
        frappe.log_error(f"Error evaluating formula '{formula}': {str(e)}", 'Salary Formula Evaluation Error')
        return None

def extract_variables_from_formula(formula):
    if formula:
        tree = ast.parse(formula, mode='eval')
        return {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    return set()

def evaluate_formula_parts(formula, variables):
    try:
        pattern = re.compile(r'\((.*?)\)\s*if\s*(.*?)\s*else\s*(.*)')
        match = pattern.match(formula)
        if match:
            true_expr = match.group(1)
            condition_expr = match.group(2)
            false_expr = match.group(3)

            condition_result = eval_salary_formula(condition_expr, variables)
            if condition_result:
                return eval_salary_formula(true_expr, variables), None
            else:
                return eval_salary_formula(false_expr, variables), None
        else:
            value = eval_salary_formula(formula, variables)
            return value, None
    except Exception as e:
        return None, f"Error evaluating formula '{formula}': {str(e)}"

class SalaryStructureAssignment(Document):
    # def before_save(self):
    #     emp = self.employee
    #     base = self.base

    #     employee_doc = frappe.get_doc('Employee', emp)
    #     payroll_category = employee_doc.get("custom_payroll_category")
    #     working_days = employee_doc.get("custom_standard_working_days")
    #     daily_rate = employee_doc.get("custom_daily_rate")

    #     if payroll_category and working_days and payroll_category=='Monthly':
    #         per_day_encashment = base/working_days
    #         self.custom_leave_encashment_amount_per_day = per_day_encashment
            
        
    #     elif payroll_category and daily_rate and payroll_category=='Daily':
    #         self.custom_leave_encashment_amount_per_day = daily_rate
            

    def on_submit(self):
        emp = self.employee
        base = self.base

        employee_doc = frappe.get_doc('Employee', emp)
                

        sal_structure_doc = frappe.get_doc('Salary Structure', self.salary_structure)
        employee_doc.reload()  

        employee_doc.get("custom_earnings").clear()
        employee_doc.get("custom_deductions").clear()

        employee_meta = frappe.get_meta('Employee')
        employee_fields = {df.fieldname: employee_doc.get(df.fieldname) for df in employee_meta.get('fields')}

        employee_doc.custom_salary_structure_assignment = self.name
        employee_doc.custom_salary_structure = self.salary_structure
        employee_doc.custom_gross_salary_per_month = base


        variables = {
            'base': base,
            'employee': emp,
        }
        variables.update(employee_fields)

        evaluated_earnings = {}
        evaluated_deductions = {}
        error_messages = []

        # Evaluate earnings
        for component in sal_structure_doc.earnings:
            salary_component = component.get('salary_component')
            abbr = component.get('abbr')
            formula = component.get('formula')
            condition = component.get('condition')

            try:
                if formula is None:
                    error_messages.append(f"Formula is missing for component '{salary_component}'.")
                    continue

                if condition:
                    condition_result = eval_salary_formula(condition, variables)
                    if not condition_result:
                        continue

                value, formula_error = evaluate_formula_parts(formula, variables)
                if formula_error:
                    error_messages.append(f"{formula_error}")
                else:
                    if value is not None:
                        evaluated_earnings[salary_component] = value
                        variables[abbr] = value
                    else:
                        error_messages.append(f"Formula evaluation returned None for component '{salary_component}' with formula '{formula}'.")

            except Exception as e:
                error_messages.append(f"Error evaluating formula or condition for component '{salary_component}' with formula '{formula}': {str(e)}")

        # Update Employee custom_earnings child table
        if not error_messages:
            for salary_component, value in evaluated_earnings.items():
                new_earning = employee_doc.append("custom_earnings", {})
                new_earning.salary_component = salary_component
                new_earning.amount = value

            # Ensure all deductions are cleared and updated
            for component in sal_structure_doc.deductions:
                salary_component = component.get('salary_component')
                abbr = component.get('abbr')
                formula = component.get('formula')
                condition = component.get('condition')

                try:
                    if formula is None:
                        error_messages.append(f"Formula is missing for deduction component '{salary_component}'.")
                        continue

                    if condition:
                        condition_result = eval_salary_formula(condition, variables)
                        if not condition_result:
                            continue

                    value, formula_error = evaluate_formula_parts(formula, variables)
                    if formula_error:
                        error_messages.append(f"{formula_error}")
                    else:
                        if value is not None:
                            evaluated_deductions[salary_component] = value
                            variables[abbr] = value
                        else:
                            error_messages.append(f"Formula evaluation returned None for deduction component '{salary_component}' with formula '{formula}'.")

                except Exception as e:
                    error_messages.append(f"Error evaluating formula or condition for deduction component '{salary_component}' with formula '{formula}': {str(e)}")

            if not error_messages:
                for salary_component, value in evaluated_deductions.items():
                    new_deduction = employee_doc.append("custom_deductions", {})
                    new_deduction.salary_component = salary_component
                    new_deduction.amount = value

            employee_doc.save()

        # if error_messages:
        #     for error in error_messages:
        #         frappe.msgprint(error)
        # else:
        #     frappe.msgprint(f"Final Evaluated Values: {variables}")
