frappe.pages['neft-details'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'NEFT Details',
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
                renderHTMLForm(company_name, from_date, to_date,employee_name);
            }
        }
        else{
            renderHTMLForm(company_name, from_date, to_date, employee_name);
        }
    });

    $(fromdateField.$input).on('input', function() {
        var company_name = $(companyField.$input).val();
        var from_date = $(fromdateField.$input).val();
        var to_date = $(todateField.$input).val();
        
        if (!from_date && !to_date && !company_name) {
            contentContainer.html('<p>Please select From Date,To Date and Company to view data because it is mandatory field.</p>');            
        }
        else if (!from_date && !to_date) {
            contentContainer.html('<p>Please select From Date and To Date to view data because it is mandatory field.</p>');            
        } 
        else if (!from_date && !company_name) {
            contentContainer.html('<p>Please select From Date and Company to view data because it is mandatory field.</p>');            
        } 
        else{
            contentContainer.html('<p>Please select From Date to view data because it is mandatory field.</p>');    
        }
    });
    
    $(todateField.$input).on('input', function() {
        var company_name = $(companyField.$input).val();
        var from_date = $(fromdateField.$input).val();
        var to_date = $(todateField.$input).val();
        
        if (!from_date && !to_date && !company_name) {
            contentContainer.html('<p>Please select From Date,To Date and Company to view data because it is mandatory field.</p>');            
        }
        else if (!to_date && !from_date) {
            contentContainer.html('<p>Please select To Date and From Date to view data because it is mandatory field.</p>');            
        } 
        else if (!to_date && !company_name) {
            contentContainer.html('<p>Please select To Date and Company to view data because it is mandatory field.</p>');     
        } 
        else{
            contentContainer.html('<p>Please select To Date to view data because it is mandatory field.</p>'); 
        }
    });

    $(employeeField.$input).on('input', function() {
        var company_name = $(companyField.$input).val();
        var from_date = $(fromdateField.$input).val();
        var to_date = $(todateField.$input).val();
        var employee_filter = $(employeeField.$input).val();
        
        if (!employee_filter && from_date && to_date && company_name) {
           console.log("No available")
           getEmployeeData(employee_filter);
        }
        
    });
    
    $(companyField.$input).on('input', function() {
        var company_name = $(this).val();
        var from_date = $(fromdateField.$input).val();
        var to_date = $(todateField.$input).val();
        
        if (!company_name && !from_date && !to_date) {
            contentContainer.html('<p>Please select From Date,To Date and Company to view data because it is mandatory field.</p>');            
        }
        else if (!company_name && !from_date) {
            contentContainer.html('<p>Please select Company and From Date to view data because it is mandatory field.</p>');            
        } 
        else if (!company_name && !to_date) {
            contentContainer.html('<p>Please select Company and To Date to view data because it is mandatory field.</p>');            
        } 
        else{
            contentContainer.html('<p>Please select Company to view data because it is mandatory field.</p>');    
        }
    });

   // JavaScript code
    $(employeeField.$input).on('awesomplete-selectcomplete', function() {
        var company_name = $(companyField.$input).val();
        var from_date = $(fromdateField.$input).val();
        var to_date = $(todateField.$input).val();
        var employee_name = $(this).val(); 
        if (employee_name && !from_date && to_date &&company_name ) {
            contentContainer.html('<p>Please select From Date to view data because it is mandatory field.</p>');                        
        }
        else if (employee_name && !to_date && from_date && company_name) {
            contentContainer.html('<p>Please select To Date to view data because it is mandatory field.</p>');            
        } 
        else if (employee_name && !to_date && !from_date && company_name) {
            contentContainer.html('<p>Please select From Date and To Date to view data because it is mandatory field.</p>');            
        } 
        else if (employee_name && to_date && !from_date && !company_name) {
            contentContainer.html('<p>Please select From Date and Company to view data because it is mandatory field.</p>');            
        } 
        else if (employee_name && !to_date && from_date && !company_name) {
            contentContainer.html('<p>Please select To Date and Company to view data because it is mandatory field.</p>');            
        } 
        else if (employee_name && !company_name && from_date && to_date) {
            contentContainer.html('<p>Please select Company to view data because it is mandatory field.</p>');            
        } 
        else if (employee_name && !from_date && !to_date && !company_name) {
            contentContainer.html('<p>Please select From date, To Date and Company to view data because it is mandatory field.</p>');            
        } 
        else{
            getEmployeeData(employee_name);
        }
    });

    function getEmployeeData(employeeName) {
        var company_name = companyField.get_value();
        var from_date = fromdateField.get_value();
        var to_date = todateField.get_value();
        renderHTMLForm(company_name, from_date, to_date, employeeName);
    }

    frappe.call({
        method: 'mumal_hr.mumal_hr.page.neft_details.neft_details.default_field_value',
        callback: function(response) {
            var data = response.message;
            if (data && data.length === 3) {
                var monthStartDate = data[0];
                var monthEndDate = data[1];
                var defaultCompany = data[2];

                fromdateField.set_input(monthStartDate);
                todateField.set_input(monthEndDate);
                companyField.set_value(defaultCompany);

                $(fromdateField.$input).trigger('change');
                $(todateField.$input).trigger('change');

                renderHTMLForm(defaultCompany, monthStartDate, monthEndDate); 
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
            if (company_name && !employee_name) {
                renderHTMLForm(company_name, from_date, to_date, employee_name);
                var fromDateObj = frappe.datetime.user_to_obj(from_date);
    
                var to_date = new Date(fromDateObj.getFullYear(), fromDateObj.getMonth() + 1, 0);
                var to_date_str = frappe.datetime.obj_to_str(to_date);
        
                todateField.set_input(to_date_str);
        
                $(todateField.$input).trigger('change');
            } else if (!company_name && !employee_name) {
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
        if (from_date && to_date) {
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
    
        
    });
    

    function renderHTMLForm(companyName, from_date, to_date, employeeName) {
        if (companyName) {
            var formattedFromDate = frappe.datetime.str_to_user(from_date);
            var formattedToDate = frappe.datetime.str_to_user(to_date);
            frappe.call({
                method: 'mumal_hr.mumal_hr.page.neft_details.neft_details.get_all_company_data',
                args: {
                    company_name: companyName,
                    from_date: formattedFromDate,
                    to_date: formattedToDate,
                    employee_name: employeeName
                },
                callback: function(r) {
                    if (r.message) {
                        var company = r.message.company;
                        var fromDate = formattedFromDate;
                        var parts = fromDate.split('-');
                        var dateObject = new Date(parts[2], parts[1] - 1, parts[0]); // Create Date object

                        var monthName = dateObject.toLocaleString('en-US', { month: 'long' }).toUpperCase();
                        var year = dateObject.getFullYear(); // Get full year

                        var formatted_from_date = `${monthName} - ${year}`;
                        var rendered_html = frappe.render_template('neft_details', { company: company, from_date: formatted_from_date, to_date: formattedToDate });
                        contentContainer.html(rendered_html); 
                        $(page.wrapper).find('.page-title').remove();

                        var printButton = $('<button>').text('Print').addClass('btn btn-primary');
                        printButton.on('click', function() {
                            window.print();
                        });
                        $('.page-actions').empty().append(printButton);

                        getAttendanceData(companyName, from_date, to_date, employeeName); 
                        
                        // Log default company name to console
                        console.log('Default Company:', company);
                    }
                }
            });
        }
    }

    // Declare totalRow globally
    var totalRow = '';
    function getAttendanceData(companyName, from_date, to_date, employeeName) {
        function getCurrentDate() {
            var today = frappe.datetime.get_today();
            var formattedDate = frappe.datetime.str_to_user(today);

            return formattedDate;
        }
        frappe.call({
            method: 'mumal_hr.mumal_hr.page.neft_details.neft_details.get_attendance_data',
            args: {
                company_name: companyName,
                from_date: from_date,
                to_date: to_date,
                employee_name: employeeName
            },
            callback: function(r) {
                if (r.message && r.message.length > 0) {
                    var attendanceRows = '';
                    var totalAmount = 0; // Initialize total amount variable

                    r.message.forEach(function(attendance, index) {
                        var rowNumber = index + 1;
                        var bankAccountNo = attendance.bank_account_no ? attendance.bank_account_no : '';
                        var amount = attendance.net_pay ? format_currency(attendance.net_pay, frappe.defaults.get_default("currency")) : '';
                        var amountWords = attendance.total_in_words ? attendance.total_in_words : '';
                        attendanceCompany = attendance.company;
                        attendanceRows += '<tr>' +
                            '<td style="padding: 4px;">' + rowNumber + '</td>' +
                            '<td style="padding: 4px;">' + attendance.employee_name + '</td>' +
                            '<td style="padding: 4px;">' + bankAccountNo + '</td>' +
                            '<td style="padding: 4px;">' + amount + '</td>' +
                            '<td style="padding: 4px;">' + amountWords + '</td>' +
                            '</tr>';

                        // Calculate total amount
                        totalAmount += parseFloat(attendance.net_pay);
                    });

                    // Call the server-side method to convert totalAmount to words
                    frappe.call({
                        method: 'mumal_hr.mumal_hr.page.neft_details.neft_details.convert_to_words',
                        args: {
                            amount: totalAmount
                        },
                        callback: function(r) {
                            var totalAmountWords = r.message;

                            // Construct total row HTML
                            totalRow = '<tr>' +
                                '<td><b></b></td>' +
                                '<td colspan="2" style="padding: 4px 8px; text-align:right; font-size: 13px !important;"><b>Grand Total</b></td>' +
                                '<td style="font-size: 13px !important;"><b>' + format_currency(totalAmount, frappe.defaults.get_default("currency")) + '</b></td>' +
                                '<td style="padding: 4px;">' + totalAmountWords + '</td>' +
                                '</tr>';
                                updateTotalRow();
                                updateHTMLContent(attendanceRows, totalAmount, totalAmountWords)
                                // console.log(attendanceCompany)
                               // Fetch and update company address
                                fetchCompanyAddress(attendanceCompany, function(companyAddress) {
                                    // Update company-related elements
                                    $('#header_company_name').text(attendanceCompany);
                                    $('#footer_company_info').text('FOR: ' + attendanceCompany);
                                    $('#header_company_address').html(companyAddress);
                                });
                                var currentDate = getCurrentDate();
                                $('#current_date').html('<b>Date: </b>' + currentDate);
                            }
                    });
                    $('#attendance_table_body').html(attendanceRows);
                    // $('#total_row').html(totalRow).show();
                } else {
                    // No attendance data found scenario
                    $('#attendance_table_body').html('<tr><td colspan="12" style="text-align:center;">No data found</td></tr>');
                    $('#total_row').hide();
                }
            }
        });
    }
    function fetchCompanyAddress(companyName, callback) {
        // Call custom API endpoint to fetch company address
        frappe.call({
            method: 'mumal_hr.mumal_hr.page.neft_details.neft_details.get_company_address', // Replace with your actual API endpoint
            args: {
                company_name: companyName
            },
            callback: function(r) {
                if (r.message && r.message.address) {
                    var addressData = r.message.address;
        
                    var addressParts = [];
        
                    if (addressData.address_line1) addressParts.push(addressData.address_line1.trim().replace(/[,\.]+$/, ''));
                    if (addressData.address_line2) addressParts.push(addressData.address_line2.trim().replace(/[,\.]+$/, ''));
                    if (addressData.city) addressParts.push(addressData.city.trim().replace(/[,\.]+$/, ''));
                    if (addressData.state) addressParts.push(addressData.state.trim().replace(/[,\.]+$/, ''));
                    if (addressData.pincode) addressParts.push(addressData.pincode.trim().replace(/[,\.]+$/, ''));
                    if (addressData.country) addressParts.push(addressData.country.trim().replace(/[,\.]+$/, ''));
        
                    var contactParts = [];
        
                    if (addressData.phone) contactParts.push(`<b>Phone:</b> ${addressData.phone.trim().replace(/[,\.]+$/, '')}`);
                    if (addressData.fax) contactParts.push(`<b>Fax:</b> ${addressData.fax.trim().replace(/[,\.]+$/, '')}`);
                    if (addressData.email_id) contactParts.push(`<b>Email:</b> ${addressData.email_id.trim().replace(/[,\.]+$/, '')}`);
        
                    var fullAddress = addressParts.filter(Boolean).join(', ');
                    var fullContact = contactParts.filter(Boolean).join(', ');
        
                    if (fullContact) {
                        fullAddress += (fullAddress ? '<br/>' : '') + fullContact;
                    }
        
                    callback(fullAddress);
                } else {
                    console.log('Company address not found.');
                }
            }
        });
    }
       

    function updateHTMLContent(attendanceRows, totalAmount, totalAmountWords) {
        var attendanceTableRows = $('#attendance_table_body').find('td').length;
        // Update attendance table body
        if (attendanceTableRows > 1) {
            if (totalAmountWords.endsWith('.')) {
                totalAmountWords = totalAmountWords.slice(0, -1); // Remove last character
            }
            // Update cheque amount paragraph
            var chequeAmountText = 'WE ARE ENCLOSING HEREWITH CHEQUE NO._________ DATED-___________ FOR ' + format_currency(totalAmount, frappe.defaults.get_default("currency")) + '  (' + totalAmountWords.toUpperCase() + ') TOWARDS ABOVE PAYMENT OF SALARY TO THE ABOVE MENTIONED EMPLOYEES.';
            // Replace placeholder with actual amount
            chequeAmountText = chequeAmountText.replace('295766.00', format_currency(totalAmount, frappe.defaults.get_default("currency")));
            
            $('#cheque_amount_paragraph').text(chequeAmountText);
        }
        else{
            // Update cheque amount paragraph
            var chequeAmountText = 'WE ARE ENCLOSING HEREWITH CHEQUE NO._________ DATED-___________ FOR AMOUNT (AMOUNT IN WORD) TOWARDS ABOVE PAYMENT OF SALARY TO THE ABOVE MENTIONED EMPLOYEES.';
            // Replace placeholder with actual amount
            chequeAmountText = chequeAmountText.replace('295766.00', format_currency(totalAmount, frappe.defaults.get_default("currency")));
            
            $('#cheque_amount_paragraph').text(chequeAmountText);
        }
    }
    
    function updateTotalRow() {
        // Check if attendanceRows (table body) has content
        var attendanceTableRows = $('#attendance_table_body').find('td').length;

        if (attendanceTableRows > 1) { // Checking for more than one row (header row is included)
            $('#total_row').html(totalRow).show(); // Show total row if attendanceRows is not empty
        } else {
            $('#total_row').hide(); // Hide total row if attendanceRows is empty
        }
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
