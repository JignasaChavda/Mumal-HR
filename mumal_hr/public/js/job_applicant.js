frappe.ui.form.on('Job Applicant', {
    refresh: function(frm) {
        // Add the custom button on the form
        frm.add_custom_button(__('Create Job Offer'), function() {
            // Action to create a new Job Applicant record
            frappe.new_doc('Job Offer', {
                job_applicant: frm.doc.email_id,
                job_title: frm.doc.name, 
                job_opening: frm.doc.name,
                applicant_name: frm.doc.applicant_name,
                applicant_email: frm.doc.email_id,
                designation: frm.doc.designation,
                company: frm.doc.custom_company
            });
        }); 
    },
    on_submit: function(frm) {
        // Make the interview_details child table read-only after the form is submitted
        frm.fields_dict['interview_details'].grid.get_field('fieldname').df.read_only = 1;
        frm.fields_dict['interview_details'].grid.refresh();
    }
});

