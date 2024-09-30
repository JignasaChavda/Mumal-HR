app_name = "mumal_hr"
app_title = "Mumal HR"
app_publisher = "jignasha@sanskartechnolab.com"
app_description = "Mumal HR"
app_email = "jignasha@sanskartechnolab.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mumal_hr/css/mumal_hr.css"
# app_include_js = "/assets/mumal_hr/js/mumal_hr.js"

# include js, css files in header of web template
# web_include_css = "/assets/mumal_hr/css/mumal_hr.css"
# web_include_js = "/assets/mumal_hr/js/mumal_hr.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mumal_hr/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# hooks.py in your ERPNext app
doctype_js = {
    "Employee": "public/js/employee.js",
    "Training Feedback": "public/js/training_feedback.js",
    "Exit Interview": "public/js/exit_interview.js",
    "Job Opening": "public/js/job_opening.js",
    "Job Applicant": "public/js/job_applicant.js",
    "Interview": "public/js/interview.js",
    "Interview Feedback": "public/js/interview_feedback.js",
    "Employee Bonus":"public/js/employee_bonus.js",
    # "Employee Increment":"public/js/employee_increment.js"
}


# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
doctype_list_js = {"Employee" : "public/js/employee_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "mumal_hr.utils.jinja_methods",
# 	"filters": "mumal_hr.utils.jinja_filters"
# }
# custom_hrms/custom_hrms/hooks.py



# Installation
# ------------

# before_install = "mumal_hr.install.before_install"
# after_install = "mumal_hr.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "mumal_hr.uninstall.before_uninstall"
# after_uninstall = "mumal_hr.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "mumal_hr.utils.before_app_install"
# after_app_install = "mumal_hr.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "mumal_hr.utils.before_app_uninstall"
# after_app_uninstall = "mumal_hr.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mumal_hr.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Interview": "mumal_hr.overrides.interview.Interview",
    "Job Offer": "mumal_hr.overrides.job_offer.CustomJobOffer",
    "Salary Slip": "mumal_hr.overrides.salary_slip.SalarySlip",
    "Salary Structure Assignment": "mumal_hr.overrides.salary_structure_assignment.SalaryStructureAssignment"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# doc_events = {
#     'Employee Increment': {
#         'on_submit': 'mumal_hr.api.auto_create_salary_structure_assignment'
#     }
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"mumal_hr.tasks.all"
# 	],
# 	"daily": [
# 		"mumal_hr.tasks.daily"
# 	],
# 	"hourly": [
# 		"mumal_hr.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mumal_hr.tasks.weekly"
# 	],
# 	"monthly": [
# 		"mumal_hr.tasks.monthly"
# 	],
# }

scheduler_events = {
    "cron": {
        "0 0 * * *": [
            "mumal_hr.api.birthday_reminder", #Every day 12:00 Midnight in Run
            "mumal_hr.api.work_anniversary_reminder", #Every day 12:00 Midnight in Run
            "mumal_hr.api.create_salary_structure_assignments"
        ],
        "0 16 * * *": [
            "mumal_hr.api.create_salary_structure_assignments", #Every day 04:00 PM Run
        ],
        "50 23 * * *": [
            "mumal_hr.api.mark_attendance"
        ]
    }
}



# Testing
# -------

# before_tests = "mumal_hr.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"hrms.hr.doctype.job_applicant.job_applicant.create_interview": "mumal_hr.overrides.job_applicant.create_interview"}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "mumal_hr.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["mumal_hr.utils.before_request"]
# after_request = ["mumal_hr.utils.after_request"]

# Job Events
# ----------
# before_job = ["mumal_hr.utils.before_job"]
# after_job = ["mumal_hr.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"mumal_hr.auth.validate"
# ]
fixtures = [
    {"dt":"Custom Field","filters":[
        [
            "module","in",[
                "Mumal HR"
            ]
        ]
    ]},
    {"dt":"Property Setter","filters":[
        [
            "module","in",[
                "Mumal HR"
            ]
        ]
    ]},
    {"dt":"Client Script","filters":[
        [
            "module","in",[
                "Mumal HR"
            ]
        ]
    ]},
    {"dt":"Server Script","filters":[
        [
            "module","in",[
                "Mumal HR"
            ]
        ]
    ]},
    {"dt":"Print Format","filters":[
        [
            "module","in",[
                "Mumal HR"
            ]
        ]
    ]}

]