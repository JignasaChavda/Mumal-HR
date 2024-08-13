
//Create without button get html page
frappe.pages['f16-page'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: '',
        single_column: true
    });

    // Create a container for the filter
    var filterContainer = $('<div>').appendTo(page.body);

    // Create a container for the page content
    var contentContainer = $('<div>').appendTo(page.body);

    var employeeField = frappe.ui.form.make_control({
        df: {
            label: 'Employee',
            fieldtype: 'Link',
            options: 'Employee',
            fieldname: 'employee_filter'
        },
        parent: filterContainer,
        render_input: true
    });
    employeeField.make();
    $(employeeField.$input_area).css({
        'width': '250px', // Adjust width as needed
        'border': '1px solid #ccc',
        'border-radius': '5px', // Add border radius
        'margin-right': '20px'
    });

    var fulllnameField = frappe.ui.form.make_control({
        df: {
            label: 'Full Name',
            fieldtype: 'Data',
            fieldname: 'full_name',
            hidden: true,
            read_only: 1
        },
        parent: filterContainer,
        render_input: true
    });
    fulllnameField.make();
    $(fulllnameField.$input).css({
        'width': '250px', // Adjust width as needed
        'border': '2px solid #ccc',
        'border-radius': '5px' // Add border radius
    });

    filterContainer.css({
        'display': 'flex',
        'align-items': 'center' // Optional: Align items vertically centered
    });

    // Attach event listener to employee field to log "Hello" on selection from the list
    $(employeeField.$input_area).find('input').on('awesomplete-select', function() {
        var employeevalue =  employeeField.label;
        console.log(employeevalue);
        console.log(employeeField);
        if (employeevalue) {
            fulllnameField.df.hidden = false;
            fulllnameField.refresh(); 
            fulllnameField.set_input("AAA");
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Employee',
                    name: employeevalue
                },
                callback: function(response) {
                    var employee = response.message;
                    if (employee && employee.employee_name) {
                        var employeeName = employee.employee_name;
                        console.log(employeeName); // Log the first name of the employee
                        fulllnameField.set_input(employeeName)
                        frappe.call({
                            method: 'mumal_hr.mumal_hr.page.f16_page.f16_page.get_employee_details',  // Assuming you have this method defined
                            args: {
                                employee: employeevalue
                            },
                            callback: function(response) {
                                var result = response.message;
                                if (result.middle_name && result.last_name) {
                                    father_name = result.middle_name + " " + result.last_name;
                                } else {
                                    father_name = ""
                                }
                                
                                var rendered_html = frappe.render_template('f16_page', {
                                    employee_name: result.employee_name,
                                    employee_id: result.employee_id,
                                    middle_name: result.middle_name,
                                    last_name: result.last_name,
                                    employee_name: result.employee_name,
                                    department: result.department,
                                    date_of_joining: result.date_of_joining,
                                    father_name: father_name
                                });
                
                                // Render the HTML content inside the content container
                                contentContainer.html(rendered_html);
                
                                // Add print button and remove the default one
                                var printButton = $('<button>').text('Print').addClass('btn btn-primary');
                                printButton.on('click', function() {
                                    printContent();
                                });
                                $('.page-actions').empty().append(printButton);
                            }
                        });
                    }
                }
            });
            
        } else {
            fulllnameField.df.hidden = true; // Hide department field
            fulllnameField.refresh(); // Refresh the field to apply changes
        }
        
    });

    // Function to print content without filter
    function printContent() {
        // Hide filter container before printing
        filterContainer.hide();

        // Print the content
        window.print();

        // Show filter container after printing
        filterContainer.show();
    }

    // Remove the default print button
    $(document).on('app_ready', function() {
        $('.page-actions .btn-print').remove();
    });

    // Add print styles to hide filter container
    var printStyle = $('<style>').text('@media print { .page-actions, .page-body > div:first-child { display: none; } }');
    $('head').append(printStyle);

    // Check if the page is being loaded from the browser history
    $(window).on('popstate', function() {
        // Reload the page
        window.location.reload();
    });
};



