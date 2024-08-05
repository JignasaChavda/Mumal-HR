frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        // console.log(frm.doc.name);

        // Function to remove the button
        function remove_button() {
            if (frm.custom_buttons && frm.custom_buttons['Send Welcome Email']) {
                frm.custom_buttons['Send Welcome Email'].remove();
            }
        }

        // Function to add the button and set up its click handler
        function add_button() {
            if (!frm.custom_buttons || !frm.custom_buttons['Send Welcome Email']) {
                frm.add_custom_button(__('Send Welcome Email'), function() {
                    if (frm.doc.status !== 'Active') {
                        frappe.msgprint(__('This employee is not an active employee. Therefore, the welcome email will not be sent.'));
                        // console.log('Employee status is not Active.');
                        return;
                    }

                    // Disable the button immediately
                    let button = frm.custom_buttons['Send Welcome Email'];
                    if (button) {
                        button.prop('disabled', true); // jQuery method to disable button
                        button.addClass('disabled'); // Add a class for styling purposes
                    }

                    // Call the server-side function to send a welcome email
                    frappe.call({
                        method: 'mumal_hr.api.send_welcome_emails',
                        args: {
                            current_employee_name: frm.doc.name
                        },
                        callback: function(r) {
                            if (r.message) {
                                // Show a detailed success message
                                frappe.show_alert({
                                    message: __('Welcome email sent successfully to {0}.', [frm.doc.employee_name]),
                                    indicator: 'green'
                                });

                                // Update the form field to reflect that the email has been sent
                                frm.set_value('custom_welcome_mail_sent', 1);

                                // Save the form to persist changes
                                frm.save().then(() => {
                                    // Refresh the form after saving
                                    frm.reload_doc().then(() => {
                                        // Remove the button after successful email sending
                                        remove_button();
                                    });
                                });
                            } else {
                                // Show an error message
                                frappe.show_alert({
                                    message: __('There was an error sending the welcome email.'),
                                    indicator: 'red'
                                });

                                // Re-enable the button if there's an error
                                if (frm.custom_buttons && frm.custom_buttons['Send Welcome Email']) {
                                    frm.custom_buttons['Send Welcome Email'].prop('disabled', false);
                                    frm.custom_buttons['Send Welcome Email'].removeClass('disabled');
                                }
                            }
                        }
                    });
                });
            }
        }

        // Function to toggle the button based on `custom_welcome_mail_sent`
        function toggle_button() {
            if (frm.is_new()) {
                remove_button(); // Remove the button if the form is new
            } else if (frm.doc.custom_welcome_mail_sent) {
                remove_button(); // Remove the button if email has been sent
            } else {
                add_button(); // Add the button if email hasn't been sent and form is not new
            }
        }

        // Initially check the status of the checkbox
        toggle_button();

        // Add a listener for changes to the `custom_welcome_mail_sent` field
        frm.fields_dict['custom_welcome_mail_sent'].df.onchange = function() {
            toggle_button();
        };
    }
});



