import frappe

def execute(filters=None):
    columns, data = [], []
    if filters:
        # Get filter values
        training_event = filters.get("training_event")
        feedback_template = filters.get("feedback_template")
        employee = filters.get("employee")
        
        # Fetch filtered feedback data
        if training_event and feedback_template:
            feedback_data = get_filtered_training_feedback_data(training_event, feedback_template, employee)
        else:
            feedback_data = []
        
        # Define columns dynamically
        num_records = len(feedback_data)
        
        # Add the "Points" column manually with width 600
        columns.append({
            "fieldname": "points", 
            "label": "<b>Points</b>",  # Centered and bold
            "fieldtype": "Data", 
            "width": 600
        })

        # Define remaining columns with custom width of 100
        columns.extend([
            {
                "fieldname": f"column_{i}", 
                "label": f"<b><center>{i}</center></b>",  # Centered and bold
                "fieldtype": "Data", 
                "width": 100
            } 
            for i in range(1, num_records + 1)
        ])

        # Prepare data
        # Add headers for Employee IDs
        data.append(["<b>Employee ID</b>"] + [f"<center>{record['employee_id']}</center>" for record in feedback_data])
        # Add headers for Employee Names
        data.append(["<b>Employee Name</b>"] + [f"<center>{record['employee_name']}</center>" for record in feedback_data])
        # Add headers for Feedback IDs
        # data.append(["<b>Feedback ID</b>"] + [f"<center>{record['feedback_name']}</center>" for record in feedback_data])

        # Add rows for each question in the template
        if feedback_template:
            template = frappe.get_doc("Training Feedback Questionnaire Template", feedback_template)
            for question in template.feedback_questionnaire:
                question_text = f"{question.question_english} / {question.question_hindi}"
                question_row = [question_text]
                
                # Populate the feedback values for this question
                for record in feedback_data:
                    answer_value = record['answers'].get(question.question_english, '0')
                    
                    # Format answer value based on its type
                    try:
                        answer_float = float(answer_value)
                        if answer_float.is_integer():
                            formatted_answer = f"{int(answer_float)}"  # Display as integer if no decimal part
                        else:
                            formatted_answer = f"{answer_float:.1f}"  # Display as float with one decimal place
                    except ValueError:
                        formatted_answer = answer_value  # Keep original value if it's not a number
                    
                    question_row.append(f"<center>{formatted_answer}</center>")

                data.append(question_row)
    
    return columns, data

@frappe.whitelist()
def get_filtered_training_feedback_data(training_event, feedback_template, employee=None):
    # Fetch feedback data that matches the specified training_event and feedback_template
    filters = {
        'training_event': training_event,
        'custom_training_feedback_questionnaire_template': feedback_template
    }
    if employee:
        filters['employee'] = employee
    
    feedback_records = frappe.get_all(
        'Training Feedback',
        fields=['name', 'employee'],
        filters=filters
    )
    
    feedback_data = []
    for record in feedback_records:
        employee_id = record.employee
        employee_name = frappe.get_value('Employee', employee_id, 'employee_name')
        feedback_id = record.name
        
        # Fetch feedback answers for this feedback record
        answers = frappe.get_all(
            'Training Feedback Answers',
            fields=['question_english', 'answer'],  # Use 'answer' instead of 'answer_value'
            filters={'parent': feedback_id}
        )
        
        # Create a dictionary for answers
        answer_dict = {answer['question_english']: answer['answer'] for answer in answers}
        
        feedback_data.append({
            "feedback_name": feedback_id,
            "employee_id": employee_id,
            "employee_name": employee_name,
            "answers": answer_dict
        })
    
    return feedback_data

@frappe.whitelist()
def get_default_template(training_event=None):
    # Check if a training_event is provided and exists
    if training_event and frappe.db.exists('Training Event', training_event):
        # Fetch the default Training Feedback Questionnaire Template
        default_template = frappe.get_all('Training Feedback Questionnaire Template', fields=['name'], limit=0)
        print(default_template)
        # if default_template:
        #     return default_template[0].name
    # Return None if no default template or training_event doesn't exist
    return default_template

@frappe.whitelist()
def get_first_training_event():
    # Fetch the first Training Event based on creation date
    training_event = frappe.get_all('Training Event', fields=['name', 'start_time','end_time', 'company'], order_by='creation desc', limit=0)
    if training_event:
        return {
            'name': training_event[0].name,
            'start_time': training_event[0].start_time,
            'company': training_event[0].company,
            'end_time': training_event[0].end_time,
        }
    return None

@frappe.whitelist()
def get_templates_for_event(training_event=None):
    # Determine the filter based on the presence of training_event
    if training_event:
        filters = {'training_event': training_event}
    else:
        filters = {'training_event': ''}  # Default filter when no training_event is provided
    
    # Fetch and return the templates based on the determined filters
    return frappe.get_all('Training Feedback Questionnaire Template', 
                          filters=filters, 
                          fields=['name'])

@frappe.whitelist()
def get_training_event_details(training_event):
    # Fetch the start_time and company of the specified Training Event
    training_event_data = frappe.get_value('Training Event', training_event, ['start_time', 'company', 'end_time'])
    
    if training_event_data:
        return {
            'start_time': training_event_data[0],
            'company': training_event_data[1],
            'end_time': training_event_data[2]
        }
    return None

@frappe.whitelist()
def get_default_template():
    # Fetch the default Training Feedback Questionnaire Template
    default_template = frappe.get_all('Training Feedback Questionnaire Template', fields=['name'], limit=1)
    if default_template:
        return default_template[0].name
    return None


