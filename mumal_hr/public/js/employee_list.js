frappe.listview_settings['Employee'] = {
    onload: function(list_view) {
        let send_button = null;

        function remove_button() {
            if (send_button) {
                send_button.remove();
                send_button = null;
            }
        }

        function add_button() {
            if (!send_button) {
                send_button = list_view.page.add_inner_button(__('Send Welcome Email'), function() {
                    const selected_items = list_view.get_checked_items();

                    if (selected_items.length === 0) {
                        frappe.msgprint(__('Please select at least one active employee.'));
                        return;
                    }

                    const employee_names = selected_items.map(item => item.name);

                    // Disable the button immediately
                    send_button.prop('disabled', true);
                    send_button.addClass('disabled');

                    frappe.call({
                        method: 'frappe.client.get_list',
                        args: {
                            doctype: 'Employee',
                            filters: { name: ['in', employee_names] },
                            fields: ['name', 'custom_welcome_mail_sent', 'status']
                        },
                        callback: function(r) {
                            if (r.message) {
                                const active_employees = r.message.filter(employee => employee.status === 'Active');
                                
                                if (active_employees.length === 0) {
                                    frappe.msgprint(__('Please select only active employees.'));
                                    send_button.prop('disabled', false);
                                    send_button.removeClass('disabled');
                                    return;
                                }

                                const employees_to_email = active_employees.filter(employee => employee.custom_welcome_mail_sent === 0)
                                                                            .map(employee => employee.name);
                                
                                if (employees_to_email.length === 0) {
                                    frappe.msgprint(__('Selected employees have already been sent a welcome email.'));
                                    send_button.prop('disabled', false);
                                    send_button.removeClass('disabled');
                                    return;
                                }

                                // console.log('Employees to be emailed:', employees_to_email);

                                // Send emails and update `custom_welcome_mail_sent` field
                                const email_promises = employees_to_email.map(employee_name => {
                                    return new Promise((resolve, reject) => {
                                        frappe.call({
                                            method: 'mumal_hr.api.send_welcome_emails',
                                            args: {
                                                current_employee_name: employee_name
                                            },
                                            callback: function(r) {
                                                if (r.message) {
                                                    resolve(employee_name);
                                                } else {
                                                    reject(employee_name);
                                                }
                                            },
                                            error: function(err) {
                                                reject(new Error(`API call failed: ${err}`));
                                            }
                                        });
                                    });
                                });

                                Promise.all(email_promises).then((email_results) => {
                                    // Prepare to update `custom_welcome_mail_sent` field for active employees only
                                    const update_promises = email_results.map(employee_name => {
                                        return frappe.call({
                                            method: 'frappe.client.set_value',
                                            args: {
                                                doctype: 'Employee',
                                                name: employee_name,
                                                fieldname: 'custom_welcome_mail_sent',
                                                value: 1
                                            }
                                        });
                                    });

                                    return Promise.all(update_promises);
                                }).then(() => {
                                    // Notify success and refresh the list view
                                    frappe.msgprint(__('All welcome emails sent and records updated successfully.'));
                                    window.location.reload();                                     
                                }).catch((error) => {
                                    // console.error('Error:', error);
                                    frappe.msgprint(__('There was an error sending some emails or updating records.'));
                                }).finally(() => {
                                    // Re-enable the button after the process is complete
                                    send_button.prop('disabled', false);
                                    send_button.removeClass('disabled');
                                });
                            }
                        }
                    });
                });
            }
        }

        add_button();
    }
};
