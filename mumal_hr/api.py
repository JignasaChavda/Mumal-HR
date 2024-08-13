import frappe
from frappe.utils import nowdate
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def birthday_reminder():
    # Get today's date in yyyy-mm-dd format
    today = nowdate()
    
    # Convert today's date to datetime.date object
    today_date = datetime.strptime(today, '%Y-%m-%d').date()
    today_day_month = today_date.strftime('%d-%m')

    # Check HR Settings for the birthday greetings setting
    hr_settings = frappe.get_single('HR Settings')
    if not hr_settings.send_birthday_reminders:
        return "Birthday checkbox is disabled in HR Settings."

    # Fetch all employees
    employee_list = frappe.get_list(
        'Employee',
        filters={'status': 'Active'},
        fields=['name', 'company', 'employee_name', 'date_of_birth', 'prefered_contact_email', 'personal_email', 'user_id', 'image'],
        limit_page_length=0  # Fetch all records
    )

    result = []
    for employee in employee_list:
        # Convert date_of_birth to datetime.date object
        if employee.get('date_of_birth'):
            if isinstance(employee['date_of_birth'], str):
                dob_date = datetime.strptime(employee['date_of_birth'], '%Y-%m-%d').date()
            else:
                dob_date = employee['date_of_birth']
                
            dob_day_month = dob_date.strftime('%d-%m')

            # Compare day and month
            if dob_day_month == today_day_month:
                # Initialize preferred_email as None
                preferred_email = None

                # Check preferred_contact_email and get the respective email
                if employee.get('prefered_contact_email') == "Personal Email" and employee.get('personal_email'):
                    preferred_email = employee['personal_email']
                elif employee.get('user_id'):
                    # Fetch the user's email from the User doctype
                    user_email = frappe.db.get_value('User', employee['user_id'], 'email')
                    if user_email:
                        preferred_email = user_email

                # Create a dictionary with the required fields
                employee_info = {
                    'name': employee['name'],
                    'employee_name': employee['employee_name'],
                    'company': employee['company'],
                    'date_of_birth': employee['date_of_birth'],
                    'email': preferred_email,
                    'image': employee['image']
                }

                # Add the employee_info to the result list
                result.append(employee_info)

                # Fetch default email account
                email_account = frappe.get_doc("Email Account", {"default_outgoing": 1})
                default_email_account = email_account.email_id

                if preferred_email:
                    # Check if image URL is available
                    image_url = employee.get('image')

                    # Create the email body with or without the employee image
                    if image_url:
                        email_body = f"""
                        <p>Dear <b>{employee['employee_name']}</b>,</p>
                        <p><img src="{image_url}" alt="Employee Image" style="max-width: 100px; height: auto;" /></p>
                        <p>{employee['company']} family members wish you a Happy Birthday & Many Happy Returns of the Day. May you have health, happiness & prosperity.</p>
                        <p>God Bless you & your family</p>
                        <p>Regards,<br>{employee['company']} Family</p>
                        """
                    else:
                        email_body = f"""
                        <p>Dear <b>{employee['employee_name']}</b>,</p>
                        <p>{employee['company']} family members wish you a Happy Birthday & Many Happy Returns of the Day. May you have health, happiness & prosperity.</p>
                        <p>God Bless you & your family</p>
                        <p>Regards,<br>{employee['company']} Family</p>
                        """
                        
                    # Set the subject with the company name
                    subject = f"Birthday Greetings From {employee['company']} Family"

                    try:
                        frappe.sendmail(
                            recipients=[preferred_email],
                            subject=subject,
                            message=email_body,
                            sender=default_email_account,
                            expose_recipients='header',
                            now=True
                        )
                        frappe.log("Email sent successfully to {}".format(preferred_email))
                    except Exception as e:
                        frappe.log_error(f"Failed to send email to {preferred_email}: {str(e)}")

    return today, result

@frappe.whitelist(allow_guest=True)
def work_anniversary_reminder():
    def get_ordinal(n):
        """Convert an integer into its ordinal representation"""
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"

    # Get today's date in yyyy-mm-dd format
    today = nowdate()
    
    # Convert today's date to datetime.date object
    today_date = datetime.strptime(today, '%Y-%m-%d').date()
    today_day_month = today_date.strftime('%d-%m')

    # Check HR Settings for the work anniversary reminders setting
    hr_settings = frappe.get_single('HR Settings')
    if not hr_settings.send_work_anniversary_reminders:
        return "Work Anniversaries checkbox is disabled in HR Settings."

    # Fetch all employees
    employee_list = frappe.get_list(
        'Employee',
        filters={'status': 'Active'},
        fields=['name', 'company', 'employee_name', 'date_of_joining', 'prefered_contact_email', 'personal_email', 'user_id', 'image'],
        limit_page_length=0  # Fetch all records
    )

    result = []
    for employee in employee_list:
        # Convert date_of_joining to datetime.date object
        if employee.get('date_of_joining'):
            if isinstance(employee['date_of_joining'], str):
                doj_date = datetime.strptime(employee['date_of_joining'], '%Y-%m-%d').date()
            else:
                doj_date = employee['date_of_joining']
                
            doj_day_month = doj_date.strftime('%d-%m')

            # Skip sending email if the joining date is today or in the future
            if doj_date >= today_date:
                continue

            # Compare day and month
            if doj_day_month == today_day_month:
                # Calculate the number of years
                years = today_date.year - doj_date.year
                ordinal_years = get_ordinal(years)

                # Initialize preferred_email as None
                preferred_email = None

                # Check preferred_contact_email and get the respective email
                if employee.get('prefered_contact_email') == "Personal Email" and employee.get('personal_email'):
                    preferred_email = employee['personal_email']
                elif employee.get('user_id'):
                    # Fetch the user's email from the User doctype
                    user_email = frappe.db.get_value('User', employee['user_id'], 'email')
                    if user_email:
                        preferred_email = user_email

                # Create a dictionary with the required fields
                employee_info = {
                    'name': employee['name'],
                    'employee_name': employee['employee_name'],
                    'company': employee['company'],
                    'date_of_joining': employee['date_of_joining'],
                    'email': preferred_email,
                    'image': employee['image']
                }

                # Add the employee_info to the result list
                result.append(employee_info)

                # Fetch default email account
                email_account = frappe.get_doc("Email Account", {"default_outgoing": 1})
                default_email_account = email_account.email_id

                if preferred_email:
                    # Check if image URL is available
                    image_url = employee.get('image')

                    # Create the email body with or without the employee image
                    if image_url:
                        email_body = f"""
                        <p>Dear <b>{employee['employee_name']}</b>,</p>
                        <p><img src="{image_url}" alt="Employee Image" style="max-width: 100px; height: auto;" /></p>
                        <p>Congratulations on your {ordinal_years} year work anniversary with us!<br> Your dedication and hard work have been a huge part of our success. Thank you for all you do. Here's to many more years of achievements and milestones together!</p>                        
                        <p>Regards,<br>{employee['company']} Family</p>
                        """
                    else:
                        email_body = f"""
                        <p>Dear <b>{employee['employee_name']}</b>,</p>
                        <p>Congratulations on your {ordinal_years} year work anniversary with us!<br> Your dedication and hard work have been a huge part of our success. Thank you for all you do. Here's to many more years of achievements and milestones together!</p>                        
                        <p>Regards,<br>{employee['company']} Family</p>
                        """
                        
                    # Set the subject with the company name
                    subject = f"Work Anniversary Greetings From {employee['company']} Family"

                    # Uncomment the following lines to actually send the email
                    try:
                        frappe.sendmail(
                            recipients=[preferred_email],
                            subject=subject,
                            message=email_body,
                            sender=default_email_account,
                            expose_recipients='header',
                            now=True
                        )
                        frappe.log("Email sent successfully to {}".format(preferred_email))
                    except Exception as e:
                        frappe.log_error(f"Failed to send email to {preferred_email}: {str(e)}")

    return today, result, email_body if result else "No work anniversaries today."

from frappe.utils.background_jobs import enqueue
@frappe.whitelist()
def send_welcome_emails(current_employee_name):
    # Fetch the current employee's details
    current_employee = frappe.get_doc('Employee', current_employee_name)


    if current_employee.status != 'Active':
        frappe.log("Skipping email sending because employee status is not 'Active'.")
        return "Employee status is not 'Active'. Email not sent."
    
    current_employeename = current_employee.employee_name
    current_employee_first_name = current_employee.first_name
    current_employee_company = current_employee.company
    current_employee_gender = current_employee.gender
    current_employee_designation = current_employee.designation
    current_employee_branch = current_employee.branch
    current_employee_image = current_employee.image
    
    # Determine the greeting for the current employee
    if current_employee_gender == 'Male':
        current_employee_greeting = 'Mr.'
        person = 'him'
    elif current_employee_gender == 'Female':
        current_employee_greeting = 'Ms.'
        person = 'her'
    else:
        current_employee_greeting = ''
        person = ''

    if current_employee_designation:
        current_employee_designation = "as " + current_employee_designation
    else:
        current_employee_designation = ''

    # Fetch the first qualification from the Employee Education child table
    qualification = ''
    if current_employee.get('education'):
        qualification = "is a qualified " + current_employee.education[0].qualification + " and"

    branch = ''
    if current_employee_branch:
        branch = current_employee_branch
    else:
        branch = "our"

    # Fetch active employees
    active_employees = frappe.get_list(
        'Employee',
        filters={'status': 'Active','company': current_employee_company,'name': ['!=', current_employee_name]},
        fields=['name', 'company', 'employee_name', 'date_of_joining', 'prefered_contact_email', 'personal_email', 'user_id', 'image', 'gender']
    )

    # Fetch default email account
    email_account = frappe.get_doc("Email Account", {"default_outgoing": 1})
    default_email_account = email_account.email_id

    for employee in active_employees:
        preferred_email = None
        
        # Determine the preferred email
        if employee.get('prefered_contact_email') == "Personal Email" and employee.get('personal_email'):
            preferred_email = employee['personal_email']
        elif employee.get('user_id'):
            # Fetch the user's email from the User doctype
            user_email = frappe.db.get_value('User', employee['user_id'], 'email')
            if user_email:
                preferred_email = user_email
        
        # Skip if no valid email is found
        if not preferred_email:
            continue
        
        if current_employee_image:
            email_body = f"""
            <p>Dear <b>{employee['employee_name']}</b>,</p>
            <p><img src="{current_employee_image}" alt="Employee Image" style="max-width: 100px; height: auto;" /></p>
            <p>Welcome {current_employee_greeting} {current_employeename} new member to our {current_employee_company} Group family.</p>
            <p>{current_employee_greeting} {current_employee_first_name}  {qualification} joined {current_employee_designation}, who would be stationed at {branch} office .</p>
            <p>Kindly welcome {person} and wishing {person} a long and successful career with {current_employee_company} group.
            """
        else:
            # Construct the email body
            email_body = f"""
            <p>Dear <b>{employee['employee_name']}</b>,</p>
            <p>Welcome {current_employee_greeting} {current_employeename} new member to our {current_employee_company} Group family.</p>
            <p>{current_employee_greeting} {current_employee_first_name}  {qualification} joined {current_employee_designation}, who would be stationed at {branch} office .</p>
            <p>Kindly welcome {person} and wishing {person} a long and successful career with {current_employee_company} group.
            """
        
        try:
            # Send the email
            frappe.sendmail(
                recipients=[preferred_email],
                subject="Welcome to the Company!",
                message=email_body,
                sender=default_email_account,
                expose_recipients='header',
                now=True
            )
            # current_employee.custom_welcome_mail_sent = 1
            # current_employee.save()
            # frappe.db.commit()
            frappe.log("Email sent successfully to {}".format(preferred_email))
        except Exception as e:
            frappe.log_error(f"Failed to send email to {preferred_email}: {str(e)}")

    return active_employees

import frappe

@frappe.whitelist()
def validate_training_feedback(employee, training_event):
    # Fetch existing records based on the training_event and employee
    existing_records = frappe.get_all(
        'Training Feedback',
        filters={
            'training_event': training_event,
            'employee': employee
        },
        fields=['name'],
        limit_page_length=0
    )
    
    if existing_records:
        # Record exists
        return True
    return False

@frappe.whitelist()
def send_schedule_interview(scheduled_on=None,doc= None):
    print(scheduled_on)

    # You can perform additional logic here if needed

    # Return the values to be used in the client-side script
    return {
        "scheduled_on": scheduled_on,
        "doc":doc
    }

@frappe.whitelist()
def send_interview_email(applicant, schedule_date, from_time, to_time, location):
    # Get job applicant details
    applicant_doc = frappe.get_doc('Job Applicant', applicant)
    candidate_name = applicant_doc.applicant_name
    position_name = applicant_doc.designation
    company_name = applicant_doc.custom_company
    recipient_email = applicant_doc.email_id

    # Format the schedule_date
    schedule_date_formatted = datetime.strptime(schedule_date, '%Y-%m-%d').strftime('%d-%m-%Y')

    # Format times to AM/PM
    from_time_formatted = datetime.strptime(from_time, '%H:%M:%S').strftime('%I:%M %p')
    to_time_formatted = datetime.strptime(to_time, '%H:%M:%S').strftime('%I:%M %p')

    # Prepare email content with black text color
    subject = f"Interview Scheduled - {position_name} at {company_name}"
    
    # Conditional email message
    message = f"""
        <div style="color: black;">
            <b>Subject:</b> Interview Scheduled - {position_name} at {company_name}<br><br>
            <b>Dear {candidate_name},</b><br><br>
            We are pleased to inform you that your interview for the {position_name} role has been scheduled.<br><br>
            <b>Date:</b> {schedule_date_formatted}<br>
            <b>Time:</b> {from_time_formatted} To {to_time_formatted}<br>
    """
    
    if location:
        message += f"<b>Location:</b> {location}<br><br>"
    
    message += """
            Please confirm your availability by replying to this email.<br><br>
            We look forward to meeting you!
        </div>
    """

    # Send email using sendmail
    frappe.sendmail(
        recipients=[recipient_email],
        subject=subject,
        message=message,
        now=True
    )

    return "Email sent successfully"

@frappe.whitelist()
def send_interview_email(applicant, schedule_date, from_time, to_time, location=None):
    # Get job applicant details
    applicant_doc = frappe.get_doc('Job Applicant', applicant)
    candidate_name = applicant_doc.applicant_name
    position_name = applicant_doc.designation
    company_name = applicant_doc.custom_company
    recipient_email = applicant_doc.email_id

    # Format the schedule_date
    schedule_date_formatted = datetime.strptime(schedule_date, '%Y-%m-%d').strftime('%e %B %Y')
    from_time_formatted = datetime.strptime(from_time, '%H:%M:%S').strftime('%I:%M %p')
    to_time_formatted = datetime.strptime(to_time, '%H:%M:%S').strftime('%I:%M %p')

    # Prepare email content with conditional location line
    location_line = ""
    if location:
        location_line = f"<b>Location:</b> {location}<br><br>"
    else:
        location_line = f"<br>"
    subject = f"Interview Scheduled - {position_name} at {company_name}"
    message = f"""
        <div style="color: black; font-family: Arial, sans-serif; font-size: 14px;">
            Dear {candidate_name},<br><br>
            We are pleased to inform you that your interview for the {position_name} role has been scheduled.<br><br>
            <b>Date:</b> {schedule_date_formatted}<br>
            <b>Time:</b> {from_time_formatted} To {to_time_formatted}<br>
            {location_line}
            Please confirm your availability by replying to this email.<br><br>
            We look forward to meeting you!
        </div>
    """

    # Send email using sendmail
    frappe.sendmail(
        recipients=[recipient_email],
        subject=subject,
        message=message,
        now=True
    )

    return "Email sent successfully"

@frappe.whitelist()
def send_reschedule_interview_email(applicant, schedule_date, from_time, to_time, location=None):
    # Get job applicant details
    applicant_doc = frappe.get_doc('Job Applicant', applicant)
    candidate_name = applicant_doc.applicant_name
    position_name = applicant_doc.designation
    company_name = applicant_doc.custom_company
    recipient_email = applicant_doc.email_id

    # Format the schedule_date
    schedule_date_formatted = datetime.strptime(schedule_date, '%Y-%m-%d').strftime('%e %B %Y')
    from_time_formatted = datetime.strptime(from_time, '%H:%M:%S').strftime('%I:%M %p')
    to_time_formatted = datetime.strptime(to_time, '%H:%M:%S').strftime('%I:%M %p')

    # Prepare email content with conditional location line
    location_line = ""
    if location:
        location_line = f"<b>Location:</b> {location}<br><br>"
    else:
        location_line = f"<br>"

    subject = f"Interview Rescheduled - {position_name} at {company_name}"
    message = f"""
        <div style="color: black; font-family: Arial, sans-serif; font-size: 14px;">
            Dear {candidate_name},<br><br>
            We are pleased to inform you that your interview for the {position_name} role has been rescheduled.<br><br>
            <b>Date:</b> {schedule_date_formatted}<br>
            <b>Time:</b> {from_time_formatted} To {to_time_formatted}<br>
            {location_line}
            Please confirm your availability by replying to this email.<br><br>
            We look forward to meeting you!
        </div>
    """

    # Send email using sendmail
    frappe.sendmail(
        recipients=[recipient_email],
        subject=subject,
        message=message,
        now=True
    )

    return "Email sent successfully"

@frappe.whitelist()
def send_interview_clear_email(applicant, schedule_date):
    # Get job applicant details
    applicant_doc = frappe.get_doc('Job Applicant', applicant)
    candidate_name = applicant_doc.applicant_name
    position_name = applicant_doc.designation
    company_name = applicant_doc.custom_company
    recipient_email = applicant_doc.email_id

    # Format the schedule_date
    clear_date_formatted = datetime.strptime(schedule_date, '%Y-%m-%d').strftime('%e %B %Y')

    subject = f"Interview Result - {position_name} at {company_name}"
    message = f"""
        <div style="color: black; font-family: Arial, sans-serif; font-size: 14px;">
            Dear {candidate_name},<br><br>
            We are delighted to inform you that you have successfully cleared the interview for the position of {position_name} held on {clear_date_formatted} at {company_name}.<br><br>
            We will be in touch with the next steps shortly.<br><br>
            Congratulations once again!<br><br>
        </div>
    """

    # Send email using sendmail
    frappe.sendmail(
        recipients=[recipient_email],
        subject=subject,
        message=message,
        now=True
    )

    return "Email sent successfully"

