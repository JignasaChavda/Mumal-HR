frappe.ui.form.on('Job Opening', {
    refresh: function(frm) {
        // Add the custom button on the form
        frm.add_custom_button(__('Create Job Applicant'), function() {
            // Action to create a new Job Applicant record
            frappe.new_doc('Job Applicant', {
                job_title: frm.doc.name, // Link the job title to the new Job Applicant
                job_opening: frm.doc.name // Optional: Link Job Opening to the Job Applicant
            });
        }); // Optionally, group under "Actions" dropdown
    }
});
