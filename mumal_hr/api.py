import frappe
from frappe.utils import nowdate
from datetime import datetime

from frappe.utils.data import add_to_date



@frappe.whitelist(allow_guest=True)
def mark_attendance(date, shift):
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d').date()

    success_message_printed = False
    
    emp_records = frappe.db.get_all("Employee",
                                    filters={
                                        "status": 'Active'
                                    },
                                    fields=["employee"],
                                    )
    
    employee_checkins = {}

    for emp in emp_records:
        emp_name = emp.employee

        checkin_records = frappe.db.get_all(
            "Employee Checkin",
            filters={
                "employee": emp_name,
                "shift": shift,
                "custom_date": date
            },
            fields=["employee", "name", "custom_date", "log_type"],
            order_by="custom_date"
        )
        
        if checkin_records:
            for checkin in checkin_records:
                date_key = checkin['custom_date']
                if emp_name not in employee_checkins:
                    employee_checkins[emp_name] = {}
                if date_key not in employee_checkins[emp_name]:
                    employee_checkins[emp_name][date_key] = []
                employee_checkins[emp_name][date_key].append({
                    'name': checkin['name'],
                    'log_type': checkin['log_type']
                })
                
        # frappe.msgprint(str(employee_checkins))

        # else:
            
        #     holiday_list = frappe.db.get_value('Employee', emp_name, 'holiday_list')
        #     is_holiday = False
            
        #     if holiday_list:
        #         holiday_doc = frappe.get_doc('Holiday List', holiday_list)
        #         holidays = holiday_doc.get("holidays")
                
        #         for holiday in holidays:
        #             holiday_dt = holiday.holiday_date
        #             if date == holiday_dt:
        #                 is_holiday = True
        #                 break
            
        #     if not is_holiday:
        #         exists_atte = frappe.db.get_value('Attendance', {'employee': emp_name, 'attendance_date': date, 'docstatus': 1}, ['name'])
        #         if not exists_atte:
        #             attendance = frappe.new_doc("Attendance")
        #             attendance.employee = emp_name
        #             attendance.attendance_date = date
        #             attendance.shift = shift
        #             attendance.status = "Absent"
        #             attendance.custom_remarks = "No Checkin found"
        #             attendance.insert(ignore_permissions=True)
        #             attendance.submit()
        #             frappe.db.commit()

    # Extract and print values from employee_checkins dictionary
    for emp_name, dates in employee_checkins.items():
        for checkin_date, logs in dates.items():
            first_chkin = None
            last_chkout = None

            for log in logs:
                name = log['name']
                log_type = log['log_type']

                if log_type == "IN" and first_chkin is None:
                    first_chkin = name

                if log_type == "OUT":
                    last_chkout = name
            
            # Print using frappe.msgprint
            # frappe.msgprint(f"Employee: {emp_name}, Date: {checkin_date}, First Check-in: {first_chkin}, Last Checkout: {last_chkout}")
            
            if first_chkin and last_chkout:
                exists_atte = frappe.db.get_value('Attendance', {'employee': emp_name, 'attendance_date': checkin_date, 'docstatus': 1}, ['name'])
                if not exists_atte:
                    
                    chkin_datetime = frappe.db.get_value('Employee Checkin', first_chkin, 'time')
                    chkout_datetime = frappe.db.get_value('Employee Checkin', last_chkout, 'time')

                    chkin_time = frappe.utils.get_time(chkin_datetime)
                    chkout_time = frappe.utils.get_time(chkout_datetime)

                    attendance = frappe.new_doc("Attendance")
                    attendance.employee = emp_name
                    attendance.attendance_date = checkin_date
                    attendance.shift = shift
                    attendance.in_time = chkin_datetime
                    attendance.out_time = chkout_datetime
                    attendance.check_in_time = chkin_time
                    attendance.check_out_time = chkout_time
                    attendance.custom_employee_checkin = first_chkin
                    attendance.custom_employee_checkout = last_chkout
                    attendance.status = "Present"

                    attendance.insert(ignore_permissions=True)
                    attendance.submit()
                    frappe.db.commit()

                    if not success_message_printed:
                        frappe.msgprint("Attendance is Marked Successfully")
                        success_message_printed = True
                else:
                    
                    formatted_date = checkin_date.strftime("%d-%m-%Y")
                    attendance_link = frappe.utils.get_link_to_form("Attendance", exists_atte)
                    frappe.msgprint(f"Attendance already marked for Employee:{emp_name} for date {formatted_date}: {attendance_link}")

            elif first_chkin and not last_chkout:
                exists_atte = frappe.db.get_value('Attendance', {'employee': emp_name, 'attendance_date': checkin_date, 'docstatus': 1}, ['name'])
                if not exists_atte:
                    chkin_datetime = frappe.db.get_value('Employee Checkin', first_chkin, 'time')
                    chkin_time = frappe.utils.get_time(chkin_datetime)

                    attendance = frappe.new_doc("Attendance")
                    attendance.employee = emp_name
                    attendance.attendance_date = checkin_date
                    attendance.shift = shift
                    attendance.in_time = chkin_datetime
                    attendance.check_in_time = chkin_time
                    attendance.custom_employee_checkin = first_chkin
                    attendance.status = "Half Day"
                    attendance.custom_remarks = "No OutPunch"

                    attendance.insert(ignore_permissions=True)
                    attendance.submit()
                    frappe.db.commit()

                    if not success_message_printed:
                        frappe.msgprint("Attendance is Marked Successfully")
                        success_message_printed = True
                else:
                    formatted_date = checkin_date.strftime("%d-%m-%Y")
                    attendance_link = frappe.utils.get_link_to_form("Attendance", exists_atte)
                    
                    frappe.msgprint(f"Attendance already marked for Employee:{emp_name} for date {formatted_date}: {attendance_link}")

  

@frappe.whitelist(allow_guest=True)
def set_attendance_date():
    
    yesterday_date = add_to_date(datetime.now(), days=-1)
    date = yesterday_date.strftime('%Y-%m-%d')
    
    shift_types = frappe.get_all("Shift Type", filters={'enable_auto_attendance':1},fields=['name'])
    if shift_types:
        for shifts in shift_types:
            shift = shifts.name

            mark_attendance(date, shift)





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

# Employee Bonus Code

@frappe.whitelist()
def get_employee_bonus_details(employee, from_date, to_date, salary_component):

    # Retrieve the custom_bonus_calculation_criteria from the Salary Component
    sc_doc = frappe.get_doc('Salary Component', salary_component)

    custom_bonus_calculation_criteria = sc_doc.custom_bonus_calculation_criteria
    custom_bonus_percentage = sc_doc.custom_bonus_percentage

    bonus_percentage = (custom_bonus_percentage / 100)

    # Fetch the Salary Slips of the selected employee that fall within the date range and are submitted
    salary_slips = frappe.get_all(
        "Salary Slip",
        filters={
            "employee": employee,
            "start_date": [">=", from_date],  # Start date should be on or after the from_date
            "end_date": ["<=", to_date],      # End date should be on or before the to_date
            "docstatus": 1                    # Only consider submitted Salary Slips
        },
        fields=["payment_days", "start_date"]
    )
    
    total_payment_days = 0
    total_bonus_calculated = 0
    
    # Calculate total payment days and bonus for each slip
    for slip in salary_slips:
        payment_days = slip.get("payment_days", 0)
        start_date = slip.get("start_date")
        
        # Calculate the total days in the month of the slip's start date
        total_days_in_month = frappe.utils.get_last_day(start_date).day
        
        # Calculate the bonus for this salary slip using the custom criteria
        bonus_for_slip = (custom_bonus_calculation_criteria / total_days_in_month) * payment_days
        
        total_payment_days += payment_days
        total_bonus_calculated += bonus_for_slip
    
    # Perform the additional calculation (8.33% of the total_bonus_calculated)
    calculated_bonus_amount = total_bonus_calculated * bonus_percentage
    
    # Return the values, total payment days, and the calculated bonus
    return {
        'employee': employee,
        'from_date': from_date,
        'to_date': to_date,
        'total_payment_days': total_payment_days,
        'bonus_calculated_on': total_bonus_calculated,
        'calculated_bonus_amount': calculated_bonus_amount
    }

# Auto Create Salary Structure Assignment Based On Employee Increment

import frappe
from frappe.utils import today

@frappe.whitelist()
def create_salary_structure_assignments():

    # Check if the feature is enabled in HR Settings
    hr_settings = frappe.get_single('HR Settings')
    if not hr_settings.custom_auto_salary_structure_assignment:
        frappe.throw("HR Setting 'Auto Salary Structure Assignment' is disabled.")
    
    # Fetch all Employee Increment records where applicable_from is today
    increments = frappe.get_all('Employee Increment',
                                filters={'applicable_from': today(), 'docstatus': 1},
                                fields=['name', 'employee', 'applicable_from', 'new_gross'])
    
    if not increments:
        return "No Employee Increments found for today."
    
    # Process each increment record
    for increment_data in increments:
        try:
            # Fetch the last submitted Salary Structure Assignment for the employee
            last_assignment = frappe.get_all('Salary Structure Assignment',
                                             filters={'employee': increment_data['employee'], 'docstatus': 1},
                                             fields=['salary_structure'],
                                             order_by='creation desc',
                                             limit=1)
            
            if not last_assignment:
                frappe.msgprint(f"No previous Salary Structure Assignment found for employee {increment_data['employee']}.")
                continue
            
            # Use the salary_structure from the last submitted assignment
            salary_structure = last_assignment[0].get('salary_structure')
    
            # Create a new Salary Structure Assignment
            salary_structure_assignment = frappe.get_doc({
                'doctype': 'Salary Structure Assignment',
                'employee': increment_data['employee'],  
                'salary_structure': salary_structure, 
                'from_date': increment_data['applicable_from'], 
                'base': increment_data['new_gross']
            })
    
            # Insert and submit the new Salary Structure Assignment
            salary_structure_assignment.insert()
            salary_structure_assignment.submit()
            frappe.db.commit()  # Commit the transaction

            frappe.msgprint(f"New Salary Structure Assignment created and submitted for employee {increment_data['employee']}.")

        except Exception as e:
            frappe.log_error(message=str(e), title="Salary Structure Assignment Error")
            frappe.msgprint(f"Error creating and submitting Salary Structure Assignment for employee {increment_data['employee']}: {str(e)}")

    return "Salary Structure Assignments created and submitted successfully."


# @frappe.whitelist()
# def create_salary_structure_assignments():
#     # Fetch all Employee Increment records where applicable_from is today
#     increments = frappe.get_all('Employee Increment',
#                                 filters={'applicable_from': today(), 'docstatus': 1},
#                                 fields=['name','employee', 'applicable_from','new_gross'])
    

#     for increment in increments:
#         # Create Salary Structure Assignment for each record
#         try:
#             auto_create_salary_structure_assignment(frappe.get_doc('Employee Increment', increment.name))
#         except Exception as e:
#             frappe.log_error(message=str(e), title="Salary Structure Assignment Error")

# @frappe.whitelist()
# def auto_create_salary_structure_assignment(doc, args=None):
#     # Check if the feature is enabled in HR Settings
#     hr_settings = frappe.get_single('HR Settings')
#     if not hr_settings.custom_auto_salary_structure_assignment:
#         frappe.throw("HR Setting 'Auto Salary Structure Assignment' is disabled.") 
    
#     # Fetch the last submitted Salary Structure Assignment for the employee
#     last_assignment = frappe.get_all('Salary Structure Assignment',
#                                      filters={'employee': doc.employee, 'docstatus': 1},
#                                      fields=['salary_structure'],
#                                      order_by='creation desc',
#                                      limit=1)
    
#     if not last_assignment:
#         frappe.throw("No previous Salary Structure Assignment found for this employee.")

#     # Use the salary_structure from the last submitted assignment
#     salary_structure = last_assignment[0].get('salary_structure')

#     # Create a new Salary Structure Assignment
#     salary_structure_assignment = frappe.get_doc({
#         'doctype': 'Salary Structure Assignment',
#         'employee': doc.employee,  
#         'salary_structure': salary_structure, 
#         'from_date': doc.applicable_from, 
#         'base': doc.new_gross
#     })

#     salary_structure_assignment.insert()
#     frappe.msgprint("New Salary Structure Assignment created successfully.")

