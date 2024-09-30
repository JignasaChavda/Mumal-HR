frappe.ui.form.on('Employee Bonus', {
    before_save: function(frm) {
        // Check if the form is new and required fields are filled
        if (frm.doc.employee && frm.doc.from_date && frm.doc.to_date && frm.doc.salary_component) {
            
            // Function to format dates in d-m-y format
            const formatDate = (dateStr) => {
                const date = new Date(dateStr);
                const day = String(date.getDate()).padStart(2, '0');
                const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
                const year = date.getFullYear();
                return `${day}-${month}-${year}`;
            };

            // Call server-side method to calculate total payment days and bonus
            return frappe.call({
                method: 'mumal_hr.api.get_employee_bonus_details',
                args: {
                    employee: frm.doc.employee,
                    from_date: frm.doc.from_date,
                    to_date: frm.doc.to_date,
                    salary_component: frm.doc.salary_component
                },
                async: false, // Blocking call
                callback: function(r) {
                    if (r.message) {
                        if (r.message.total_payment_days === 0) {
                            // Display alert if no salary slips were found
                            const formattedFromDate = formatDate(frm.doc.from_date);
                            const formattedToDate = formatDate(frm.doc.to_date);
                            frappe.msgprint(__(`No Salary Slip found for Employee: ${frm.doc.employee} in ${formattedFromDate} to ${formattedToDate}`))
                            // frappe.msgprint((`${frm.doc.employee} salary slip not found in ${formattedFromDate} to ${formattedToDate}`));
                            frappe.validated = false; // Prevent saving the form
                        } 
                        else {
                            // Update fields on the form based on the server response
                            frm.set_value('total_days', r.message.total_payment_days);
                            frm.set_value('bonus_calculated_on', r.message.bonus_calculated_on);
                            frm.set_value('bonus_amount', r.message.calculated_bonus_amount);
                        }
                    }
                }
            });
        }
    }
});
