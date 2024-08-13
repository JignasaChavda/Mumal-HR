frappe.pages['f13'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'F13',
        single_column: true
    });

    var filterContainer = $('<div>').addClass('company-filter-area').appendTo(page.main);
    var contentContainer = $('<div>').addClass('content-area').appendTo(page.main);

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
        renderHTMLForm(company_name, employee_name);
    });

    $(employeeField.$input).on('awesomplete-selectcomplete', function() {
        var employee_name = $(this).val();
        getEmployeeData(employee_name);
    });

    function getEmployeeData(employeeName) {
        var company_name = companyField.get_value();
        renderHTMLForm(company_name, employeeName);
    }

    frappe.call({
        method: 'mumal_hr.mumal_hr.page.f13.f13.get_default_company',
        callback: function(response) {
            var defaultCompany = response.message;
            if (defaultCompany) {
                companyField.set_value(defaultCompany);
                renderHTMLForm(defaultCompany, null);
            }
        }
    });

    function renderHTMLForm(companyName, employeeName) {
        frappe.call({
            method: 'mumal_hr.mumal_hr.page.f13.f13.get_all_company_data',
            args: {
                company_name: companyName,
                employee_name: employeeName
            },
            callback: function(r) {
                if (r.message) {
                    var company = r.message.company;
                    var rendered_html = frappe.render_template('f13', { company: company });
                    contentContainer.html(rendered_html);
                    $(page.wrapper).find('.page-title').remove();

                    var printButton = $('<button>').text('Print').addClass('btn btn-primary');
                    printButton.on('click', function() {
                        window.print();
                    });
                    $('.page-actions').empty().append(printButton);

                    getAttendanceData(companyName, employeeName);
                }
            }
        });
    }

    function getAttendanceData(companyName, employeeName) {
        frappe.call({
            method: 'mumal_hr.mumal_hr.page.f13.f13.get_employee_data',
            args: {
                company_name: companyName,
                employee_name: employeeName
            },
            callback: function(r) {
                console.log(r)
                if (r.message && r.message.length > 0) {
                    var attendanceRows = '';
                    r.message.forEach(function(attendance, index) {
                        attendanceRows += '<tr>' +
                            '<td style="padding: 4px;">' + (index + 1) + '</td>' +
                            '<td style="padding: 4px;">' + (attendance.employee_name || '') + '</td>' +
                            '<td style="padding: 4px;">' + (attendance.current_address || '') + '</td>' +
                            '<td style="padding: 4px;"></td>' +
                            '<td style="padding: 4px;"></td>' +
                            '<td style="padding: 4px;"></td>' +
                            '<td style="padding: 4px;"></td>' +
                            '<td style="padding: 4px;"></td>' +
                            '<td style="padding: 4px;"></td>' +
                            '</tr>';
                    });
                    $('#attendance_table_body').html(attendanceRows);
                } else {
                    $('#attendance_table_body').html('<tr><td colspan="16" style="text-align:center;">No data found</td></tr>');
                }
            }
        });
    }
    

    $(document).on('app_ready', function() {
        $('.page-actions .btn-print').remove();
    });

    var printStyle = $('<style>').text('@media print { .page-actions, .page-body > div:first-child { display: none; } .company-filter-area { display: none !important; } .employee-filter { display: none !important; } }');
    $('head').append(printStyle);

    $(window).on('popstate', function() {
        window.location.reload();
    });
};
