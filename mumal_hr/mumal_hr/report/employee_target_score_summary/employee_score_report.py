import frappe

@frappe.whitelist()
def fetch_additional_data(from_date, to_date, user):
    # Sample logic to determine visibility based on filter values
    show_additional_data = False

    if from_date and to_date and user:
        # Perform necessary operations to determine visibility
        show_additional_data = True

    if show_additional_data:
        # If additional data should be shown, prepare the additional data
        additional_data = {
            "Criteria": "Additional Criteria",
            "Planned Score": 10,
            "Actual Score": 8,
            "Actual Percentage": 80.0,
            "visible": True  # Indicate that additional data should be displayed
        }
    else:
        additional_data = {"visible": TRUE}  # Indicate that additional data should not be displayed

    return additional_data
