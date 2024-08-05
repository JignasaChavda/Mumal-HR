frappe.ui.form.on('Training Feedback', {
    training_event: function(frm) {
        // Clear the value of 'custom_training_feedback_questionnaire_template' field
        frm.set_value('custom_training_feedback_questionnaire_template', '');

        // Set the query for 'custom_training_feedback_questionnaire_template'
        frm.set_query("custom_training_feedback_questionnaire_template", function() {
            return {
                filters: {
                    'training_event': frm.doc.training_event
                }
            };
        });
    },
    validate: function(frm) {
        if (frm.is_new() || frm.doc.is_duplicated) {
            // Use a promise to ensure the validation check completes before proceeding            
            validate_training_feedback(frm);
        }
    },
    custom_training_feedback_questionnaire_template: function(frm) {
        if (frm.doc.custom_training_feedback_questionnaire_template) {
            // Inject inline CSS for disabling checkboxes
            let css = `
                <style>
                .disabled-checkbox input[type="checkbox"] {
                    pointer-events: none; /* Prevent interaction */
                    opacity: 0.5; /* Optional: visually indicate disabled state */
                }
                </style>
            `;
            // Append the CSS to the <head> section
            $('head').append(css);

            // Fetch the selected template details
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Training Feedback Questionnaire Template',
                    name: frm.doc.custom_training_feedback_questionnaire_template
                },
                callback: function(response) {
                    let template = response.message;

                    if (template) {
                        // Clear existing rows in the child table
                        frm.clear_table('custom_feedback_answers');

                        // Add new rows from the template
                        template.feedback_questionnaire.forEach(question => {
                            let row = frm.add_child('custom_feedback_answers');
                            row.question_english = question.question_english;
                            row.question_hindi = question.question_hindi;
                        });

                        // Refresh the child table to reflect changes
                        frm.refresh_field('custom_feedback_answers');

                        // Show the child table if hidden
                        frm.toggle_display('custom_feedback_answers', true);

                        // Disable the Add Row button for the child table
                        frm.fields_dict['custom_feedback_answers'].grid.wrapper.find('.grid-add-row').hide();

                        // Disable the Delete buttons for each row
                        frm.fields_dict['custom_feedback_answers'].grid.wrapper.find('.grid-delete-row').hide();

                        // Apply custom CSS to make the checkboxes non-interactive
                        frm.fields_dict['custom_feedback_answers'].grid.wrapper.find('.row-check').addClass('disabled-checkbox');

                        // Set the fields in each row to read-only, except for the 'answer' field
                        frm.fields_dict['custom_feedback_answers'].grid.grid_rows.forEach(grid_row => {
                            grid_row.docfields.forEach(field => {
                                if (field.fieldname === 'question_english' || field.fieldname === 'question_hindi') {
                                    field.read_only = 1;
                                }
                            });
                            // Refresh the row to apply the read-only setting
                            grid_row.toggle_editable(false);
                            grid_row.refresh();
                        });

                        console.log('Template applied and child table updated.');
                    } else {
                        console.log('Template not found.');
                    }
                },
                error: function(err) {
                    console.error('Error fetching template:', err);
                }
            });
        } else {
            // Clear child table when no template is selected
            frm.clear_table('custom_feedback_answers');
            frm.refresh_field('custom_feedback_answers');

            // Hide the child table
            frm.toggle_display('custom_feedback_answers', false);

            console.log('No template selected. Child table hidden.');
        }
    }    
});

function validate_training_feedback(frm) {
    // Call the server-side function to check for existing records
    frappe.call({
        method: 'mumal_hr.api.validate_training_feedback',
        args: {
            employee: frm.doc.employee,
            training_event: frm.doc.training_event
        },
        callback: function(response) {
            if (response.message) {
                frappe.msgprint({
                    title: __('Validation Error'),
                    indicator: 'red',
                    message: __('Training Feedback already exists for this employee and training event.')
                });
                frappe.validated = false; // Prevent the form from being saved
            } else {
                // No existing record, proceed with save
                console.log('No existing records found.');
            }
        }
    });
}


