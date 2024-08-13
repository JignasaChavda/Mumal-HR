frappe.pages['f11'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'F11',
        single_column: true
    });
    
    var filterContainer = $('<div>').addClass('company-filter-area').appendTo(page.main);
    var contentContainer = $('<div>').addClass('content-area').appendTo(page.main);

    var fromdateField = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Date',
            fieldname: 'fromdate_filter',
            placeholder: 'From Date'
        },
        parent: filterContainer,
        render_input: true
    });

    fromdateField.make();

    $(fromdateField.$input).css({
        'width': '250px',
        'border': '2px solid #ccc',
        'border-radius': '5px',
        'margin-right': '20px'
    });

    var todateField = frappe.ui.form.make_control({
        df: {
            fieldtype: "Date",
            default: "frappe.datetime.month_end()",
            fieldname: 'todate_filter',
            placeholder: 'To Date'
        },
        parent: filterContainer,
        render_input: true
    });

    todateField.make();
    $(todateField.$input).css({
        'width': '250px',
        'border': '2px solid #ccc',
        'border-radius': '5px',
        'margin-right': '20px'
    });

    var employeeField = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Link',
            placeholder: 'Select Employee',
            options: 'Employee',
            fieldname: 'employee_filter'
        },
        parent: filterContainer,
        render_input: true
    });

    employeeField.make();
    $(employeeField.$input_area).css({
        'width': '250px',
        'border': '2px solid #ccc',
        'border-radius': '5px',
        'margin-right': '20px'
    });

    var companyField = frappe.ui.form.make_control({
        df: {
            fieldtype: 'Link',
            placeholder: 'Select Company',
            options: 'Company',
            fieldname: 'company_filter'
        },
        parent: filterContainer,
        render_input: true
    });

    // Make the company field
    companyField.make();
    $(companyField.$input_area).css({
        'width': '250px',
        'border': '2px solid #ccc',
        'border-radius': '5px'
    });

    filterContainer.css({
        'display': 'flex',
        'align-items': 'center'
    });

    $(companyField.$input).on('awesomplete-selectcomplete', function() {
        var company_name = $(this).val(); 
        var employee_name = employeeField.get_value();
        
        var from_date = fromdateField.get_value();
        var to_date = todateField.get_value();
    
        if (company_name) {
            if (employee_name) {
                renderHTMLForm(company_name, from_date, to_date, employee_name);
            } else {
                renderHTMLForm(company_name, from_date, to_date);
            }
        }
        else{
            renderHTMLForm(company_name, from_date, to_date, employee_name);
        }
    });

   // JavaScript code
    $(employeeField.$input).on('awesomplete-selectcomplete', function() {
        var employee_name = $(this).val(); 
        getEmployeeData(employee_name);
    });

    function getEmployeeData(employeeName) {
        var company_name = companyField.get_value();
        var from_date = fromdateField.get_value();
        var to_date = todateField.get_value();
        renderHTMLForm(company_name, from_date, to_date, employeeName);
    }


    frappe.call({
        method: 'mumal_hr.mumal_hr.page.f11.f11.default_field_value',
        callback: function(response) {
            var data = response.message;
            if (data && data.length === 3) {
                var monthStartDate = data[0];
                var monthEndDate = data[1];
                var defaultCompany = data[2];

                fromdateField.set_input(monthStartDate);
                todateField.set_input(monthEndDate);

                $(fromdateField.$input).trigger('change');
                $(todateField.$input).trigger('change');


                renderHTMLForm(null, monthStartDate, monthEndDate); 
            }
        }
    });

    
    $(fromdateField.$input).on('change', function() {
        var from_date = $(this).val();
        var to_date = todateField.get_value(); 
        var company_name = companyField.get_value();
        var employee_name = employeeField.get_value(); 
    
        if (from_date && !to_date) {
            var fromDateObj = frappe.datetime.user_to_obj(from_date);
    
            var to_date = new Date(fromDateObj.getFullYear(), fromDateObj.getMonth() + 1, 0);
    
            var to_date_str = frappe.datetime.obj_to_str(to_date);
    
            todateField.set_input(to_date_str);
    
            $(todateField.$input).trigger('change');
        } else if (from_date && to_date) {
            if (!company_name && !employee_name) {
                renderHTMLForm(company_name, from_date, to_date, employee_name);
                var fromDateObj = frappe.datetime.user_to_obj(from_date);
    
                var to_date = new Date(fromDateObj.getFullYear(), fromDateObj.getMonth() + 1, 0);
                var to_date_str = frappe.datetime.obj_to_str(to_date);
        
                todateField.set_input(to_date_str);
        
                $(todateField.$input).trigger('change');
            } else if (company_name && !employee_name) {
                renderHTMLForm(company_name, from_date, to_date, employee_name);
            } else if (employee_name && !company_name) {
                renderHTMLForm(company_name, from_date, to_date, employee_name);
                
            } else {
                renderHTMLForm(company_name, from_date, to_date, employee_name);
            }
        }
    });
    
    
    $(todateField.$input).on('change', function() {
        var from_date = fromdateField.get_value();
        var to_date = todateField.get_value();
        var company_name = companyField.get_value();
        var employee_name = employeeField.get_value();
    
        if (from_date && !to_date) {
        } else if (from_date && to_date) {
            if (!company_name && !employee_name) {
                renderHTMLForm(company_name, from_date, to_date, employee_name);
            } else if (company_name && !employee_name) {
                renderHTMLForm(company_name, from_date, to_date, employee_name);
            } else if (employee_name && !company_name) {
                renderHTMLForm(company_name, from_date, to_date, employee_name);
            } else {
                renderHTMLForm(company_name, from_date, to_date, employee_name);
            }
        }
    
        renderHTMLForm(company_name, from_date, to_date, employee_name);
    });
    

function renderHTMLForm(companyName, from_date, to_date, employeeName) {
    var formattedFromDate = frappe.datetime.str_to_user(from_date);
    var formattedToDate = frappe.datetime.str_to_user(to_date);

    frappe.call({
        method: 'mumal_hr.mumal_hr.page.f11.f11.get_all_company_data',
        args: {
            company_name: companyName,
            from_date: formattedFromDate,
            to_date: formattedToDate,
            employee_name: employeeName
        },
        callback: function(r) {
            if (r.message) {
                var company = r.message.company;
                var rendered_html = frappe.render_template('f11', { company: company, from_date: formattedFromDate, to_date: formattedToDate });
                contentContainer.html(rendered_html); 
                $(page.wrapper).find('.page-title').remove();

                var printButton = $('<button>').text('Print').addClass('btn btn-primary');
                printButton.on('click', function() {
                    window.print();
                });
                $('.page-actions').empty().append(printButton);

                getAttendanceData(companyName, from_date, to_date, employeeName); 
            }
        }
    });
}

function getAttendanceData(companyName, from_date, to_date, employeeName) {
    frappe.call({
        method: 'mumal_hr.mumal_hr.page.f11.f11.get_attendance_data',
        args: {
            company_name: companyName, 
            from_date: from_date,
            to_date: to_date,
            employee_name: employeeName 
        },
        callback: function(r) {
            if (r.message && r.message.length > 0) {
                var attendanceRows = '';
                r.message.forEach(function(attendance) {
                    var dateParts = attendance.attendance_date.split('-'); 
                    var formattedDate = frappe.datetime.str_to_user(attendance.attendance_date); 
                    attendanceRows += '<tr>' +
                        '<td style="padding: 4px; width:12%;">' + attendance.employee + '</td>' +
                        '<td style="padding: 4px; width:14%;">' + attendance.employee_name + '</td>' + 
                        '<td style="padding: 4px;">' + attendance.department + '</td>' +
                        '<td style="padding: 4px;"></td>' +
                        '<td style="padding: 4px;"></td>' +
                        '<td style="padding: 4px;">' + attendance.company + '</td>' +
                        '<td style="padding: 4px;"></td>' +
                        '<td style="padding: 4px;"></td>' +
                        '<td style="padding: 4px;"></td>' +
                        '<td style="padding: 4px;"></td>' +
                        '<td style="padding: 4px;"></td>' +
                        '<td style="padding: 4px;">' + formattedDate + '</td>' + 
                        '</tr>';
                });
                $('#attendance_table_body').html(attendanceRows);
            } else {
                $('#attendance_table_body').html('<tr><td colspan="12" style="text-align:center;">No attendance data found</td></tr>');
            }
        }
    });
}


    $(document).on('app_ready', function() {
        $('.page-actions .btn-print').remove();
    });

    var printStyle = $('<style>').text('@media print { .page-actions, .page-body > div:first-child { display: none; } .company-filter-area { display: none; } }');
    $('head').append(printStyle);

    $(window).on('popstate', function() {
        window.location.reload();
    });
}
