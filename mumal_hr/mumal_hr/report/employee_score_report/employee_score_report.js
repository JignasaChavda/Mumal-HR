// Copyright (c) 2024, jignasha@sanskartechnolab.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Score Report"] = {
	"filters": [
			{
				"fieldname": "from_date",
				"label": "From Date",
				"fieldtype": "Date",
				"on_change": function() {
					var from_date = frappe.query_report.get_filter_value('from_date');
				
					if (from_date) {
						var toDateObj = frappe.datetime.add_days(from_date, 6);
						frappe.query_report.set_filter_value('to_date', toDateObj);
					}
				},		
				"reqd": 1
			},
			{
				"fieldname": "to_date",
				"label": "To Date",
				"fieldtype": "Date",
				"reqd": 1
			},
			{
				"fieldname": "user",
				"label": "User",
				"fieldtype": "Link",
				"options": "User",
				// "reqd": 1
			}
	],


	onload: function(report) {
        // Add a custom button to duplicate the report data
        report.page.add_inner_button(__("Employee Target Score Summary"), function() {
            // Retrieve filter values from the report
            var filters = report.get_values();

            // Construct the URL for the report view with filter values
            var url = "/app/query-report/Employee Target Score Summary";
            if (filters) {
                var query_params = [];
                Object.keys(filters).forEach(function(key) {
                    query_params.push(key + "=" + encodeURIComponent(filters[key]));
                });
                url += "?" + query_params.join("&");
            }

            // Open the report view URL in the same window
            window.open(url, '_self');
        });
    }
	
};
