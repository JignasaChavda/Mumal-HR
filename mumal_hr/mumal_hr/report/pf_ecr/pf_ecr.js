// Copyright (c) 2025, jignasha@sanskartechnolab.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PF ECR"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Date",
			"on_change": function() {
					var from_date = frappe.query_report.get_filter_value('from_date');
				
					if (from_date) {
						var toDateObj = moment(from_date).endOf('month').format('YYYY-MM-DD');
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
			"fieldname": "company",
			"label": "Company",
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1
		}
	],
};
