// Add page in Company Filter
frappe.pages['f12'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'FORM NO. 12',
        single_column: true
    });

    // Create a div for the filter and a div for the content
    var filterContainer = $('<div>').addClass('company-filter-area').appendTo(page.main);
    var contentContainer = $('<div>').addClass('content-area').appendTo(page.main);

    // Create a link field for company filter
    var companyField = frappe.ui.form.make_control({
        df: {
            label: 'Company',
            fieldtype: 'Link',
            options: 'Company',
            fieldname: 'company_filter'
        },
        parent: filterContainer,
        render_input: true
    });

    // Make the company field
    companyField.make();

    // Apply CSS styles to the input area
    $(companyField.$input_area).css({
        'width': '250px',
        'border': '2px solid #ccc',
        'border-radius': '5px'
    });

    // Call server-side endpoint to fetch default company
    frappe.call({
        method: 'mumal_hr.mumal_hr.page.f12.f12.get_default_company',
        callback: function(response) {
            var defaultCompany = response.message;
            if (defaultCompany) {
                companyField.set_input(defaultCompany);
                console.log('Default Company:', defaultCompany);

                // After setting the default company, trigger a change event
                $(companyField.$input).trigger('change');
                
                // Render the HTML form with the default company data
                renderHTMLForm(defaultCompany);
            }
        }
    });

    // Event listener for the company filter change
    $(companyField.$input_area).find('input').on('awesomplete-select', function() {
        var selectedCompany = companyField.label;
        console.log('Selected Company:', selectedCompany);

        // Call the server-side method to get company data
        if (selectedCompany) {
            renderHTMLForm(selectedCompany);
        } else {
            // Handle case where no company is selected
            contentContainer.html(''); // Clear only the content area
        }
    });

    function renderHTMLForm(companyName) {
        // Call the server-side method to get company data
        frappe.call({
            method: 'mumal_hr.mumal_hr.page.f12.f12.get_all_company_data',
            args: {
                company_name: companyName
            },
            callback: function(r) {
                if (r.message) {
                    var company = r.message[0];
                    var rendered_html = frappe.render_template('f12', { company: company });
                    contentContainer.html(rendered_html); // Update only the content area
                    $(page.wrapper).find('.page-title').remove();

                    // Add print button
                    var printButton = $('<button>').text('Print').addClass('btn btn-primary');
                    printButton.on('click', function() {
                        window.print();
                    });
                    $('.page-actions').empty().append(printButton);
                }
            }
        });
    }

    // Remove the default print button
    $(document).on('app_ready', function() {
        $('.page-actions .btn-print').remove();
    });

    // Add print styles to hide filter container
    var printStyle = $('<style>').text('@media print { .page-actions, .page-body > div:first-child { display: none; } .company-filter-area { display: none; } }');
    $('head').append(printStyle);

    // Check if the page is being loaded from the browser history
    $(window).on('popstate', function() {
        // Reload the page
        window.location.reload();
    });
};




// Get Default Template
// frappe.pages['f12'].on_page_load = function(wrapper) {
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'FORM NO. 12',
//         single_column: true
//     });

    // frappe.call({
    //     method: 'mumal_hr.mumal_hr.page.f12.f12.get_all_company_data',
    //     callback: function(r) {
    //         if (r.message) {
    //             var companies = r.message;
    //             var rendered_html = frappe.render_template('f12', { companies: companies });
    //             $(page.body).html(rendered_html);
    //             $(page.wrapper).find('.page-title').remove();
            
    //             var printButton = $('<button>').text('Print').addClass('btn btn-primary');
    //             printButton.on('click', function() {
    //                 window.print();
    //             });
    //             $('.page-actions').empty().append(printButton);
    //         }
    //     }
    // });
//     // Remove the default print button
//     $(document).on('app_ready', function() {
//         $('.page-actions .btn-print').remove();
//     });
    
//     // Add print styles to hide filter container
//     var printStyle = $('<style>').text('@media print { .page-actions, .page-body > div:first-child { display: none; } }');
//     $('head').append(printStyle);
    
//     // Check if the page is being loaded from the browser history
//     $(window).on('popstate', function() {
//         // Reload the page
//         window.location.reload();
//     }); 
// };

