// Copyright (c) 2024, jignasha@sanskartechnolab.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('PL Calculation', {
	refresh: function(frm) {
        frm.fields_dict['encashment_details'].grid.wrapper.on('change', 'input[data-fieldname="carry_forward"]', function(e) {
            var row = $(this).closest('[data-name]').data('name');
            var value = e.target.checked ? 1 : 0;
            frappe.model.set_value('Encashment Details', row, 'carry_forward', value);
            if (value === 1) {
                frappe.model.set_value('Encashment Details', row, 'encashment', 0);
            }
        });

        frm.fields_dict['encashment_details'].grid.wrapper.on('change', 'input[data-fieldname="encashment"]', function(e) {
            var row = $(this).closest('[data-name]').data('name');
            var value = e.target.checked ? 1 : 0;
            frappe.model.set_value('Encashment Details', row, 'encashment', value);
            if (value === 1) {
                frappe.model.set_value('Encashment Details', row, 'carry_forward', 0);
            }
        });
    },

	onload: function(frm) {
        
        frm.set_query("leave_type", function() {
            return {
                filters: {
                    'allow_encashment': 1 
                }
            };
        });
    },
	
	from_date: function (frm) {
		var from_date = frm.doc.from_date;

		if (from_date) {
			
			var to_date = frappe.datetime.add_months(from_date, 12);
			var final_to_date = frappe.datetime.add_days(to_date, -1);

			
			frm.set_value('to_date', final_to_date);
			frm.refresh_field('to_date');
		} else {
			
			frm.set_value('to_date', '');
			frm.refresh_field('to_date');
		}
	},
	next_year_start_date: function (frm) {
		var from_date = frm.doc.next_year_start_date;

		if (from_date) {
			
			var to_date = frappe.datetime.add_months(from_date, 12);
			var final_to_date = frappe.datetime.add_days(to_date, -1);

			
			frm.set_value('next_year_end_date', final_to_date);
			frm.refresh_field('next_year_end_date');
		} else {
			
			frm.set_value('next_year_end_date', '');
			frm.refresh_field('next_year_end_date');
		}
	},
	

	get_details: function(frm){
		
		if (!frm.doc.from_date || !frm.doc.to_date) {
			frappe.throw("Please Select the date range");
		} else if (!frm.doc.leave_type) {
			frappe.throw("Please Select the leave type");
		}
		
		
		if(frm.doc.from_date && frm.doc.to_date && frm.doc.leave_type){
			frappe.call({
				method: 'mumal_hr.mumal_hr.doctype.pl_calculation.pl_calculation.get_encashment_details',
				args: {
					'from_date': frm.doc.from_date,
					'to_date': frm.doc.to_date,
					'leave_type': frm.doc.leave_type
				},
				callback: function(r) {
					if (r.message) {
						
						frm.clear_table('encashment_details');
						
						
						$.each(r.message, function(employee_id, employee) {
                            var row = frm.add_child('encashment_details');
                            row.employee = employee.employee;
                            row.employee_name = employee.employee_name;
                            row.department = employee.department;
                            row.designation = employee.designation;
							row.payroll_category = employee.payroll_category
							row.present_days = employee.present_days
							row.eligible_leave = employee.eligible_leaves
							row.amount = employee.amount
							

                            
                            if (employee.salary_per_day) {
                                row.salary_per_day = employee.salary_per_day;
                            }
                            if (employee.gross_salary) {
                                row.monthly_salary = employee.gross_salary;
                            }
                            if (employee.daily_rate) {
                                row.daily_rate = employee.daily_rate;
                            }
                        });

						
						frm.refresh_field('encashment_details');
					}
				}
			});
		}	
	},
	before_submit: function(frm){
		if (!frm.doc.next_year_start_date || !frm.doc.next_year_end_date){
			frappe.throw("Please Select Next year daterange for carryforwarding leaves");
		}
		
	}
});

