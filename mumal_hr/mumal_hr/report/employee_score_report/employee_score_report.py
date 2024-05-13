import frappe

def execute(filters=None):
    # Define columns for the report
    columns = [
        {"label": "Name", "fieldname": "name", "fieldtype": "Data"},
        # {"label": "Planned Score", "fieldname": "planned_score", "fieldtype": "Int"},
        # {"label": "Actual Score", "fieldname": "actual_score", "fieldtype": "Int"},
        # {"label": "Actual Score On", "fieldname": "actual_score_on", "fieldtype": "Int"},
        {"label": "Work Not Done", "fieldname": "work_not_done", "fieldtype": "Data"},
        {"label": "Work Not Done On Time", "fieldname": "work_not_done_on_time", "fieldtype": "Data"},
        {"label": "Total Work", "fieldname": "total_work", "fieldtype": "Data"},
        {"label": "Mobile No", "fieldname": "mobile_no", "fieldtype": "Data"}
    ]

    # Initialize data as an empty list
    data = []

    # Define the base SQL query
    sql_query = """
        SELECT
            t.custom_assigned_user_name AS name,
            # COALESCE(COUNT(t.name), 0) AS planned_score,
            # COALESCE(SUM(CASE WHEN t.completed_on  THEN 1 ELSE 0 END), 0) AS actual_score,
            # COALESCE(SUM(CASE WHEN t.custom_completed_on_time <= t.custom_expected_end_time THEN 1 ELSE 0 END),0) AS actual_score_on,
            COALESCE(ROUND((SUM(CASE WHEN t.completed_on  THEN 1 ELSE 0 END)/ COUNT(t.name)) * 100-100, 2),0) AS work_not_done,
            COALESCE(ROUND(SUM(CASE WHEN t.completed_on AND t.custom_completed_on_time <= t.custom_expected_end_time THEN 1 ELSE 0 END) / SUM(CASE WHEN t.completed_on  THEN 1 ELSE 0 END) *100 -100,2),0) AS work_not_done_on_time,
            COALESCE(COUNT(t.name), 0) AS total_work,
            u.mobile_no AS mobile_no
        FROM
            `tabTask` t
        LEFT JOIN
            `tabUser` u ON t.custom_assigned_to = u.name
    """

    # Prepare the condition for filtering
    condition = ""
    params = {}

    # Check if filters are provided
    if filters:
        user = filters.get("user")
        from_date = filters.get("from_date")
        to_date = filters.get("to_date")

        # Add filtering conditions to the SQL query
        condition = """
            WHERE 1=1
        """
        params = {}

        if user:
            condition += " AND t.custom_assigned_to = %(user)s"
            params["user"] = user
        
        if from_date and to_date:
            condition += " AND t.exp_end_date BETWEEN %(from_date)s AND %(to_date)s"
            params["from_date"] = from_date
            params["to_date"] = to_date

        # Add condition to filter out rows where custom_assigned_user_name is NULL or empty
        condition += " AND t.custom_assigned_user_name IS NOT NULL AND t.custom_assigned_user_name != ''"

    # Group by custom_assigned_user_name
    group_by_clause = " GROUP BY t.custom_assigned_user_name, u.mobile_no"

    # Concatenate the condition and group by clause to the base SQL query
    final_query = sql_query + condition + group_by_clause

    # Execute SQL query with filter values
    data = frappe.db.sql(final_query, params, as_dict=True)

    # Filter out rows where custom_assigned_user_name is NULL or empty in Python (additional filtering)
    filtered_data = [row for row in data if row['name'] is not None and row['name'] != '']

    # Return columns and filtered data
    return columns, filtered_data
