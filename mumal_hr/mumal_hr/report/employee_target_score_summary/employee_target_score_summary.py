# # Copyright (c) 2024, jignasha@sanskartechnolab.com and contributors
# # For license information, please see license.txt

# import frappe

# def execute(filters=None):
#     # Define columns for the report
#     columns = [
#         {"label": "Criteria", "fieldname": "Criteria", "fieldtype": "Data"},
#         {"label": "Planned Score", "fieldname": "Planned Score", "fieldtype": "Int"},
#         {"label": "Actual Score", "fieldname": "Actual Score", "fieldtype": "Int"},
#         {"label": "Actual Percentage", "fieldname": "Actual Percentage", "fieldtype": "Data"}
#     ]

#     # Initialize data as an empty list
#     data = []

#     # Check if filters are provided
#     if filters:
#         user = filters.get("user")
#         from_date = filters.get("from_date")
#         to_date = filters.get("to_date")

#    # Define SQL query to count tasks where custom_expected_end_time is between from_date and to_date
#         sql_query = """
# 		SELECT
# 			'Work not done' AS Criteria,
# 			COALESCE(COUNT(t.name),0) AS `Planned Score`,
# 			COALESCE(SUM(CASE WHEN t.completed_on BETWEEN %(from_date)s AND %(to_date)s THEN 1 ELSE 0 END),0) AS `Actual Score`,
# 			COALESCE(ROUND((SUM(CASE WHEN t.completed_on BETWEEN %(from_date)s AND %(to_date)s THEN 1 ELSE 0 END) / COUNT(t.name)) * 100-100, 2),0) AS `Actual Percentage`
# 		FROM
# 			`tabTask` t
# 		WHERE
# 			t.custom_assigned_to = %(user)s
# 			AND t.exp_end_date BETWEEN %(from_date)s AND %(to_date)s

# 		UNION

# 		SELECT
# 			'Work not done on time' AS Criteria,
# 			COALESCE(SUM(CASE WHEN t.completed_on BETWEEN %(from_date)s AND %(to_date)s THEN 1 ELSE 0 END),0) AS `Planned Score`,
# 			COALESCE(SUM(CASE WHEN t.completed_on BETWEEN %(from_date)s AND %(to_date)s AND t.custom_completed_on_time <= t.custom_expected_end_time THEN 1 ELSE 0 END),0) AS `Actual Score`,
# 			COALESCE(ROUND((SUM(CASE WHEN t.completed_on BETWEEN %(from_date)s AND %(to_date)s AND t.custom_completed_on_time <= t.custom_expected_end_time THEN 1 ELSE 0 END) / SUM(CASE WHEN t.completed_on BETWEEN %(from_date)s AND %(to_date)s THEN 1 ELSE 0 END) * 100) - 100, 2),0) AS `Actual Percentage`
            
#         FROM
# 			`tabTask` t
# 		WHERE
# 			t.custom_assigned_to = %(user)s
# 			AND t.exp_end_date BETWEEN %(from_date)s AND %(to_date)s
   

			
#         """

#         # Execute SQL query with filter values
#         data = frappe.db.sql(sql_query, {"user": user, "from_date": from_date, "to_date": to_date}, as_dict=True)

#     # Return columns and data
#     return columns, data




import frappe

def execute(filters=None):
    # Define columns for the report
    columns = [
        {"label": "Criteria", "fieldname": "Criteria", "fieldtype": "Data"},
        {"label": "Planned Score", "fieldname": "Planned Score", "fieldtype": "Int"},
        {"label": "Actual Score", "fieldname": "Actual Score", "fieldtype": "Int"},
        {"label": "Actual Percentage", "fieldname": "Actual Percentage", "fieldtype": "Data"}
    ]

    # Initialize data as an empty list
    data = []


    # Check if filters are provided
    if filters:
        user = filters.get("user")
        from_date = filters.get("from_date")
        to_date = filters.get("to_date")

        # Define base SQL query
        sql_query = """
        SELECT
            'Work not done' AS Criteria,
            COALESCE(COUNT(t.name),0) AS `Planned Score`,
            COALESCE(SUM(CASE WHEN t.completed_on THEN 1 ELSE 0 END),0) AS `Actual Score`,
            COALESCE(ROUND((SUM(CASE WHEN t.completed_on  THEN 1 ELSE 0 END)/ COUNT(t.name)) * 100-100, 2),0) AS `Actual Percentage`
        FROM
            `tabTask` t
        WHERE
            t.custom_assigned_to = %(user)s
        """

        # Add date range condition if from_date and to_date are provided
        if from_date and to_date:
            sql_query += " AND t.exp_end_date BETWEEN %(from_date)s AND %(to_date)s"

        sql_query += """
        UNION

        SELECT
            'Work not done on time' AS Criteria,
            COALESCE(SUM(CASE WHEN t.completed_on THEN 1 ELSE 0 END),0) AS `Planned Score`,
           COALESCE(SUM(CASE WHEN t.custom_completed_on_time <= t.custom_expected_end_time THEN 1 ELSE 0 END),0) AS `Actual Score`,
            COALESCE(ROUND(SUM(CASE WHEN t.completed_on AND t.custom_completed_on_time <= t.custom_expected_end_time THEN 1 ELSE 0 END) / SUM(CASE WHEN t.completed_on  THEN 1 ELSE 0 END) *100 -100,2),0) AS `Actual Percentage`
        FROM
            `tabTask` t
        WHERE
            t.custom_assigned_to = %(user)s
        """

        # Add date range condition if from_date and to_date are provided
        if from_date and to_date:
            sql_query += " AND t.exp_end_date BETWEEN %(from_date)s AND %(to_date)s"

        # Execute SQL query with filter values
        data = frappe.db.sql(sql_query, {"user": user, "from_date": from_date, "to_date": to_date}, as_dict=True)

    else:
        # If no filters are provided, retrieve all data
        sql_query = """
        SELECT
            'Work not done' AS Criteria,
            COALESCE(COUNT(t.name),0) AS `Planned Score`,
            COALESCE(SUM(CASE WHEN t.completed_on THEN 1 ELSE 0 END),0) AS `Actual Score`,
            COALESCE(ROUND((SUM(CASE WHEN t.completed_on THEN 1 ELSE 0 END) / NULLIF(COUNT(t.name), 0) * 100), 2),0) AS `Actual Percentage`
        FROM
            `tabTask` t
        """

        sql_query += """
        UNION

        SELECT
            'Work not done on time' AS Criteria,
            COALESCE(COUNT(t.name),0) AS `Planned Score`,
            COALESCE(SUM(CASE WHEN t.completed_on THEN 1 ELSE 0 END),0) AS `Actual Score`,
            COALESCE(ROUND((SUM(CASE WHEN t.completed_on AND t.custom_completed_on_time <= t.custom_expected_end_time THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN t.completed_on THEN 1 ELSE 0 END), 0) * 100), 2),0) AS `Actual Percentage`
        FROM
            `tabTask` t
        """

        # Execute SQL query without filter values
        data = frappe.db.sql(sql_query, as_dict=True)

    # Return columns and data
    return columns, data
