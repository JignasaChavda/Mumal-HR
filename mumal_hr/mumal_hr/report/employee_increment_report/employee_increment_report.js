frappe.query_reports["Employee Increment Report"] = {
    "filters": [
        {
            "label": "Employee",
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee"
        },
        {
            "label": "Applicable From Date",
            "fieldname": "from_date",
            "fieldtype": "Date"
        },
        {
            "label": "Applicable To Date",
            "fieldname": "to_date",
            "fieldtype": "Date"
        }
    ]
};
