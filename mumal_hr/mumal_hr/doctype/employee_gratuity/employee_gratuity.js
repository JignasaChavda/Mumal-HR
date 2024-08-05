// Copyright (c) 2024, jignasha@sanskartechnolab.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Gratuity', {
    onload: function(frm) {
        // Initialize a flag to track if the message has been shown
        frm.messageShown = false;
        frm.previousEmployee = null; // Track the previous employee
    },

    employee: function(frm) {
        if (frm.doc.employee) {
            // Check if the employee has changed
            if (frm.previousEmployee !== frm.doc.employee) {
                frm.messageShown = false; // Reset the flag for the new employee
                frm.previousEmployee = frm.doc.employee;
            }

            // Perform the check and update fields if needed
            frappe.db.get_value('Employee', frm.doc.employee, 'relieving_date', (r) => {
                if (!r.relieving_date) {
                    // Show a message only if it hasn't been shown already
                    if (!frm.messageShown) {
                        let msg = frappe.msgprint({
                            title: 'Notice',
                            indicator: 'yellow',
                            message: 'The selected employee does not have a relieving date.'
                        });

                        // Set a timeout to hide the message after 1 second
                        setTimeout(() => {
                            msg.hide();
                        }, 1000); // 1 second

                        // Set the flag to true to indicate the message has been shown
                        frm.messageShown = true;
                    }

                    // Clear the total_years_of_experience field
                    frm.set_value('total_years_of_experience', '');
                } else {
                    // Reset the flag if relieving_date is available
                    frm.messageShown = false;

                    var a = frm.doc.date_of_joining;
                    var b = frm.doc.date_of_leaving;

                    // Function to format date as dd-mm-yyyy
                    function formatDate(dateString) {
                        var date = new Date(dateString);
                        var day = String(date.getDate()).padStart(2, '0');
                        var month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
                        var year = date.getFullYear();
                        return `${day}-${month}-${year}`;
                    }

                    // Function to calculate year difference as a float
                    function calculateYearDifference(date1, date2) {
                        var d1 = new Date(date1);
                        var d2 = new Date(date2);
                        var diffInMilliseconds = d2 - d1;
                        var diffInYears = diffInMilliseconds / (1000 * 60 * 60 * 24 * 365.25); // Considering leap years
                        return parseFloat(diffInYears.toFixed(1)); // Rounded to 1 decimal place
                    }

                    if (a && b) {
                        var formattedDateOfJoining = formatDate(a);
                        var formattedDateOfLeaving = formatDate(b);

                        console.log(formattedDateOfJoining, formattedDateOfLeaving); // Log the formatted dates to the console

                        // Calculate the year difference
                        var yearDifference = calculateYearDifference(a, b);

                        console.log(`Total years of experience: ${yearDifference}`); // Log the year difference

                        // Set the total_years_of_experience field with the year difference
                        frm.set_value('total_years_of_experience', yearDifference);
                    }
                }
            });
        } else {
            // Reset the flag when the employee field is cleared
            frm.messageShown = false;
            frm.previousEmployee = null; // Clear previous employee tracking
        }		
    },
    validate: function(frm) {
        console.log('Validation Check');

        // Fetch the relieving_date from the Employee doctype and perform validation
        if (frm.doc.employee) {
            frappe.db.get_value('Employee', frm.doc.employee, 'relieving_date', (r) => {
                if (!r.relieving_date) {
                    // Show popup message if relieving_date does not exist
                    frappe.msgprint({
                        title: 'Notice',
                        indicator: 'red',
                        message: 'The selected employee does not have a relieving date. The form cannot be saved.'
                    });

                    // Set the total_years_of_experience field to an empty string
                    frm.set_value('total_years_of_experience', '');

                    // Prevent the form from being saved
                    frappe.validated = false;
                } else {
                    // Additional validation for total_years_of_experience
                    if (frm.doc.total_years_of_experience < 5) {
                        frappe.msgprint({
                            title: 'Notice',
                            indicator: 'red',
                            message: `Employee: ${frm.doc.employee} (${frm.doc.employee_name}) is not eligible for gratuity as they have not completed 5 working years.`
                        });

                        // Prevent the form from being saved
                        frappe.validated = false;
                    }
                }
            });
        }
    },
    payroll_date: function(frm) {
        // Function to format date as dd-mm-yyyy
        function formatDate(dateString) {
            var date = new Date(dateString);
            var day = String(date.getDate()).padStart(2, '0');
            var month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
            var year = date.getFullYear();
            return `${day}-${month}-${year}`;
        }

        // Always reset the message flag on payroll_date change
        frm.messageShown = false;

        // Check if an employee is selected
        if (!frm.doc.employee) {
            if (!frm.messageShown && frm.doc.payroll_date) {
                // Show message only if it hasn't been shown already
                let msg = frappe.msgprint({
                    title: 'Notice',
                    indicator: 'red',
                    message: 'Please select an employee first.'
                });

                // Set a timeout to clear payroll_date if employee is not selected
                setTimeout(() => {
                    frm.set_value('payroll_date', '');
                    msg.hide();
                }, 1500);
                frm.messageShown = true; // Set the flag to true
            }
        } else {
            // Check if a salary slip exists for the selected employee
            frappe.db.get_list('Salary Slip', {
                filters: [
                    ['employee', '=', frm.doc.employee], // Filter by employee
                    ['docstatus', 'in', [0, 1]] // Filter by docstatus for Draft (0) and Submitted (1)
                ],
                fields: ['start_date', 'name', 'end_date', 'docstatus'],
                order_by: 'end_date desc' // Order by end_date in descending order to get the most recent slip first
            }).then((salarySlips) => {
                if (salarySlips.length > 0) {
                    function formatMonthYear(date) {
                        const d = new Date(date);
                        const month = (d.getMonth() + 1).toString().padStart(2, '0'); // Get month and pad with zero if needed
                        const year = d.getFullYear();
                        return { month, year }; // Return as an object with month and year
                    }
        
                    // Extract and format payroll_date
                    const payrollDate = formatMonthYear(frm.doc.payroll_date);
        
                    // Initialize a variable to keep track of the most recent matching slip
                    let mostRecentMatchingSlip = null;
        
                    salarySlips.forEach((slip) => {
                        const start = formatMonthYear(slip.start_date);
                        const end = formatMonthYear(slip.end_date);
        
                        // Check if start_date and end_date are within the same month and year
                        if (start.month === end.month && start.year === end.year) {
                            // Check if the payrollDate matches both startDate and endDate
                            if (payrollDate.month === start.month && payrollDate.year === start.year) {
                                // Update the most recent matching slip
                                mostRecentMatchingSlip = {
                                    slip_id: slip.name, // Include the Salary Slip ID
                                    payrollDate: `${payrollDate.month}-${payrollDate.year}`,
                                    start_date: `${start.month}-${start.year}`,
                                    end_date: `${end.month}-${end.year}`
                                };
                            }
                        }
                    });
        
                    // Log the most recent matching slip, if found
                    if (mostRecentMatchingSlip) {
                        console.log('Yes, match found for:', mostRecentMatchingSlip);
                    } else {
                        console.log('Payroll date does not match any salary slip start date.');
                    }
                } else {
                    console.log('No salary slips found for the selected employee.');
                }
            }).catch((error) => {
                console.error('Error fetching salary slips:', error);
            });
        }
        
        
    }
});
