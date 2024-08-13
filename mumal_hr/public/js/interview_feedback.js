frappe.ui.form.on('Interview Feedback', {
    on_submit: function(frm) {
        // Ensure that the feedback form has an associated interview
        if (frm.doc.interview) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Interview',
                    name: frm.doc.interview
                },
                callback: function(r) {
                    if (r.message) {
                        var interview = r.message;
                        var interviewer_found = false;

                        // Iterate over the interview_details child table in the Interview record
                        $.each(interview.interview_details || [], function(i, d) {
                            if (d.interviewer == frm.doc.interviewer) {
                                // Set the average_rating in interview_details to the custom_rating from the feedback form
                                d.average_rating = frm.doc.custom_rating;
                                interviewer_found = true;
                            }
                        });

                        if (interviewer_found) {
                            // Save the Interview record with the updated rating
                            frappe.call({
                                method: 'frappe.client.save',
                                args: {
                                    doc: interview
                                },
                                callback: function(res) {
                                    if (res.message) {
                                        frappe.msgprint(__('Interview details updated successfully.'));
                                    }
                                }
                            });
                        } else {
                            frappe.msgprint(__('Interviewer not found in Interview details.'));
                        }
                    }
                }
            });
        }
    }
});
