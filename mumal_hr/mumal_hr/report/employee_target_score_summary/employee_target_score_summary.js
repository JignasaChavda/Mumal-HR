frappe.query_reports["Employee Target Score Summary"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            // "reqd": 1,
            "on_change": function() {
				var from_date = frappe.query_report.get_filter_value('from_date');
			
				if (from_date) {
					var toDateObj = frappe.datetime.add_days(from_date, 6);
					frappe.query_report.set_filter_value('to_date', toDateObj);
				}
			}
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            // "reqd": 1
        },
        {
            "fieldname": "user",
            "label": "User",
            "fieldtype": "Link",
            "options": "User",
            "reqd": 1,
        }
    ],
    "onload": function(report) {
        // Set default value for the "user" filter
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'User',
                fields: ['name'],
                order_by: 'modified DESC', // Sort by creation date in descending order
                limit: 1 // Limit to one record (the most recently created user)
            },
            callback: function(response) {
                if (response && response.message && response.message.length > 0) {
                    var lastUser = response.message[0].name;
                    frappe.query_report.set_filter_value('user', lastUser);
                }
            }
        });
    }
};
