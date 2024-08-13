frappe.ui.form.on('Interview', {
    refresh: function(frm) {
        frm.set_df_property('scheduled_on', 'read_only', !frm.is_new());
        frm.set_df_property('from_time', 'read_only', !frm.is_new());
        frm.set_df_property('to_time', 'read_only', !frm.is_new());
        frm.add_custom_button(__('Submit Feedback'), function() {
            frappe.new_doc('Interview Feedback', {
                interview: frm.doc.name
            });
        });
        // Ensure this code runs after the grid has been rendered
        frm.trigger('update_interview_details_grid');
            
        if (!frm.is_new() && frm.doc.status == "Pending") {
            frm.add_custom_button(__('Interview Reschedule'), function() {
                let d = new frappe.ui.Dialog({
                    title: "Interview Reschedule",
                    fields: [
                        {
                            label: "Schedule On",
                            fieldname: "scheduled_on",
                            fieldtype: "Date",
                            reqd: 1
                        },
                        {
                            label: "From Time",
                            fieldname: "from_time",
                            fieldtype: "Time",
                            reqd: 1
                        },
                        {
                            label: "To Time",
                            fieldname: "to_time",
                            fieldtype: "Time",
                            reqd: 1
                        },
                    ],
                    primary_action_label: "Reschedule",
                    primary_action(values) {
                        cur_frm.set_value("scheduled_on",values.scheduled_on)
                        cur_frm.set_value("from_time",values.from_time)
                        cur_frm.set_value("to_time",values.to_time)
                        d.hide()
                        cur_frm.save().then(() => {                                                        
                            cur_frm.reload_doc();
                        });
                            },
                        });
                d.show();
            });
        }
        $('button[data-label="Reschedule%20Interview"]').hide();
    },

    onload: function(frm) {
        // Apply the filter to the 'interviewer' field in the child table
        frm.fields_dict['interview_details'].grid.get_field('interviewer').get_query = function() {
            return {
                query: "frappe.core.doctype.user.user.user_query", // Fetches users
                filters: {
                    enabled: 1 // Only include enabled users
                }
            };
        };
        frm.previous_scheduled_on = frm.doc.scheduled_on;
        frm.from_time = frm.doc.from_time;
        frm.to_time = frm.doc.to_time;
        frm.status = frm.doc.status;
        frm.new = frm.is_new();       
    },

    update_interview_details_grid: function(frm) {
        // Optional: Ensure the grid is fully loaded before attempting to manipulate it
        setTimeout(function() {
            if (frm.doc.docstatus == 1) {
                // Hide the "Add Row" button
                frm.fields_dict['interview_details'].grid.wrapper.find('.grid-add-row').hide();
            }       
        }, 1); 
    },
    
    after_save: function(frm) {
        // Get the current and previous values of the 'scheduled_on' field
        var currentScheduledDate = frm.doc.scheduled_on;
        var currentFromTime = frm.doc.from_time;
        var currentToTime = frm.doc.to_time;
        var currentStatus = frm.doc.status;
        var isNew = frm.new;


        var previousScheduledDate = frm.previous_scheduled_on;
        var previousFromTime = frm.from_time;
        var previousToTime = frm.to_time;
        var previousStatus = frm.status;
    
        var scheduleDateChanged = currentScheduledDate !== previousScheduledDate;
        var fromTimeChanged = currentFromTime !== previousFromTime;
        var toTimeChanged = currentToTime !== previousToTime;
        var toStatusChanged = currentStatus !== previousStatus;
    
        var status = frm.doc.status;
        var applicant = frm.doc.job_applicant;
        var applicant_name = frm.doc.custom_applicant_name;
        var fromTime = frm.doc.from_time;
        var toTime = frm.doc.to_time;
        var location = frm.doc.custom_location;
        
        if(isNew && status === "Pending"){
            var apiMethod = "mumal_hr.api.send_interview_email";
            cur_frm.reload_doc();
        }
        else{
            if(toStatusChanged && status === "Pending"){
                var apiMethod = scheduleDateChanged || fromTimeChanged || toTimeChanged ? "mumal_hr.api.send_reschedule_interview_email" : "mumal_hr.api.send_interview_email";                
                cur_frm.reload_doc();
            }
            else if(status === "Pending" && !scheduleDateChanged || !fromTimeChanged || !toTimeChanged){
                var apiMethod = scheduleDateChanged || fromTimeChanged || toTimeChanged ? "mumal_hr.api.send_reschedule_interview_email" : "";
                cur_frm.reload_doc();
            }
            else if(status === "Pending" && scheduleDateChanged || fromTimeChanged || toTimeChanged){
                var apiMethod = scheduleDateChanged || fromTimeChanged || toTimeChanged ? "mumal_hr.api.send_reschedule_interview_email" : "";
                cur_frm.reload_doc();
            }
            else{
                var apiMethod = ""
            }
        }
             
        // Call the API if status is 'Pending'
        if (status === "Pending") {
            frappe.call({
                method: apiMethod,
                args: {
                    applicant: applicant,
                    schedule_date: currentScheduledDate,
                    from_time: fromTime,
                    to_time: toTime,
                    location: location
                },
                callback: function(response) {
                    if (response.message) {
                        var msg = frappe.msgprint({
                            title: __('Success'),
                            indicator: 'green',
                            message: __('Email sent successfully to ' + applicant + ' (' + applicant_name + ')')
                        });
    
                        // Hide the message box after 2 seconds
                        setTimeout(function() {
                            msg.hide();
                        }, 2000);
                    }
                },
                error: function(error) {
                    var msg = frappe.msgprint({
                        title: __('Failed'),
                        indicator: 'red',
                        message: __('Failed to send email to ' + applicant + ' (' + applicant_name + ')')
                    });
    
                    // Hide the message box after 2 seconds
                    setTimeout(function() {
                        msg.hide();
                    }, 2000);
                }
            });
        }
    },

    
    
    
    on_submit: function(frm) {
        // Get the value of the 'status' field
        var status = frm.doc.status;
        if (status == "Cleared"){
            var applicant = frm.doc.job_applicant;
            var applicant_name = frm.doc.custom_applicant_name;
            var scheduleDate = frm.doc.scheduled_on;
            var fromTime = frm.doc.from_time;
            var toTime = frm.doc.to_time;
            var location = frm.doc.custom_location;

            frappe.call({
                method: "mumal_hr.api.send_interview_clear_email",
                args: {
                    applicant: applicant,
                    schedule_date: scheduleDate,
                    from_time: fromTime,
                    to_time: toTime,
                    location: location
                },
                callback: function(response) {
                    if (response.message) {
                        var msg = frappe.msgprint({
                            title: __('Success'),
                            indicator: 'green',
                            message: __('Email sent successfully to ' + applicant + '(' + applicant_name + ')')
                        });
    
                        setTimeout(function() {
                            msg.hide();

                        }, 2000);
                        frappe.validated = false;
                    }
                },
                error: function(error) {
                    var msg = frappe.msgprint({
                        title: __('Failed'),
                        indicator: 'Red',
                        message: __('Failed to send email to ' + applicant + '(' + applicant_name + ')')
                    });

                    setTimeout(function() {
                        msg.hide();

                    }, 2000);
                    frappe.validated = false;
                }
            });
        }
    }
});
