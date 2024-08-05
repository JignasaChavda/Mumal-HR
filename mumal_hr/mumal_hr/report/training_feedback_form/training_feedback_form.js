// Copyright (c) 2024, jignasha@sanskartechnolab.com and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Training Feedback Form"] = {
    "filters": [
        {
            "fieldname": "training_event",
            "label": "Training Event",
            "fieldtype": "Link",
            "options": "Training Event",
            "reqd": 1,          
            "on_change": function() {
                var training_event = frappe.query_report.get_filter_value('training_event');
                
                if (training_event) {
                    frappe.call({
                        method: "mumal_hr.mumal_hr.report.training_feedback_form.training_feedback_form.get_training_event_details",
                        args: {
                            "training_event": training_event
                        },
                        callback: function(response) {
                            if (response.message) {
                                var start_date = response.message.start_time.split(' ')[0];
                                var end_date = response.message.end_time.split(' ')[0];
                                frappe.query_report.set_filter_value('date', start_date);
                                frappe.query_report.set_filter_value('company', response.message.company);
                                frappe.query_report.set_filter_value('end_date', end_date);

                                // Fetch updated options for feedback_template
                                frappe.call({
                                    method: "mumal_hr.mumal_hr.report.training_feedback_form.training_feedback_form.get_templates_for_event",
                                    args: {
                                        "training_event": training_event
                                    },
                                    callback: function(response) {
                                        // console.log(response)
                                        var feedback_template_filter = frappe.query_report.get_filter('feedback_template');
                                        var templates = response.message || [];
                                        var template_names = templates.map(t => t.name);

                                        // Update feedback_template options
                                        feedback_template_filter.options = template_names;

                                        if (template_names.length > 0) {
                                            // Set the first available template as default
                                            frappe.query_report.set_filter_value('feedback_template', template_names[0]);
                                        } else {
                                            // Clear feedback_template value if no templates are available
                                            // frappe.query_report.set_filter_value('feedback_template', '');
                                            // var training_event = frappe.query_report.get_filter_value('training_event');

                                            // // Determine the filters based on the training_event value
                                            var filters = {};
                                            if (training_event) {
                                                filters = { 'training_event': ['=', ""] };
                                            }

                                            // Fetch Training Feedback Questionnaire Templates based on filters
                                            frappe.call({
                                                method: "frappe.client.get_list",
                                                args: {
                                                    doctype: "Training Feedback Questionnaire Template",
                                                    fields: ["name"],
                                                    filters: filters, // Apply filters if training_event is not null
                                                    limit_page_length: 1000,
                                                    order_by: "name desc"
                                                },
                                                callback: function(response) {
                                                    // Check if there are results
                                                    if (response.message && response.message.length > 0) {
                                                        // Get the first item from the sorted list
                                                        var first_item = response.message[0].name;
                                                        
                                                        // Set the first item as the value for feedback_template filter
                                                        var feedback_template_filter = frappe.query_report.get_filter('feedback_template');
                                                        feedback_template_filter.set_value(first_item);
                                        
                                                        // console.log("Feedback Template set to:", first_item);
                                                    } else {
                                                        // console.log("No Training Feedback Questionnaire Templates found.");
                                                    }
                                                },
                                                error: function(err) {
                                                    // console.error("Error fetching Training Feedback Questionnaire Templates:", err);
                                                }
                                            });
                                        }

                                        // Update the query for feedback_template filter
                                        feedback_template_filter.get_query = function() {
                                            return {
                                                filters: {
                                                    'training_event': ['in', [training_event, '']]
                                                }
                                            };
                                        };

                                        frappe.query_report.refresh();
                                    }
                                });
                            }
                        }
                    });
                } else {
                    frappe.query_report.set_filter_value('date', '');
                    frappe.query_report.set_filter_value('company', '');
                    frappe.query_report.set_filter_value('feedback_template', '');
                    
                    // Clear feedback_template options
                    var feedback_template_filter = frappe.query_report.get_filter('feedback_template');
                    feedback_template_filter.options = [];
                    feedback_template_filter.get_query = function() {
                        return {
                            filters: {}
                        };
                    };
                    frappe.query_report.refresh();
                }
            }
        },
        {
            "fieldname": "feedback_template",
            "label": "Training Feedback Questionnaire Template",
            "fieldtype": "Link",
            "options": "Training Feedback Questionnaire Template",
            "reqd": 1
        },
        {
            "fieldname": "date",
            "label": "Date",
            "fieldtype": "Date",
            "read_only": 1
        },
        {
            "fieldname": "end_date",
            "label": "end Date",
            "fieldtype": "Date",
            "read_only": 1
        },
        {
            "fieldname": "company",
            "label": "Company",
            "fieldtype": "Link",
            "options": "Company",
            "read_only": 1
        },
        {
            "fieldname": "employee",
            "label": "Employee",
            "fieldtype": "Link",
            "options": "Employee",
            "on_change": function() {
                frappe.query_report.refresh();  // Refresh report when employee filter changes
            }
        }
    ],
    onload: function(report) {
        frappe.call({
            method: "mumal_hr.mumal_hr.report.training_feedback_form.training_feedback_form.get_first_training_event",
            callback: function(response) {
                if (response.message) {
                    frappe.query_report.set_filter_value('training_event', response.message.name);
                    var start_date = response.message.start_time.split(' ')[0];
                    frappe.query_report.set_filter_value('date', start_date);
                    frappe.query_report.set_filter_value('company', response.message.company);

                    // Fetch and set default feedback_template based on the first training event
                    frappe.call({
                        method: "mumal_hr.mumal_hr.report.training_feedback_form.training_feedback_form.get_templates_for_event",
                        args: {
                            "training_event": response.message.name
                        },
                        callback: function(response) {
                            var feedback_templates = response.message;
                            if (feedback_templates.length > 0) {
                                frappe.query_report.set_filter_value('feedback_template', feedback_templates[0].name);
                            } else {
                                frappe.query_report.set_filter_value('feedback_template', '');
                            }

                            frappe.query_report.refresh();
                        }
                    });
                }
            }
        });
    }
};

