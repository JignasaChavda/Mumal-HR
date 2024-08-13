// frappe.pages['f29'].on_page_load = function(wrapper) {
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'F29 Page',
//         single_column: true
//     });

//     // Render the template and append it to the page body
//     $(wrapper).find('.layout-main-section').html(frappe.render_template('f29', { title: 'F29 Page' }));

//     // Hide the specific div
//     $(wrapper).find('.row.flex.align-center.page-head-content.justify-between').hide();
// }


frappe.pages['f29'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'F29 Page',
        single_column: true
    });
	

    // Fetch data from the server
    frappe.call({
        method: 'mumal_hr.mumal_hr.page.f29.f29.get_employee_details',
        callback: function(response) {
            var data = response.message;
            // Render the template and append it to the page body
			console.log("\n\n\n",data,"\n\n\n")
            $(wrapper).find('.layout-main-section').html(frappe.render_template('f29', data));
			$(page.wrapper).find('.page-title').remove();
			var printButton = $('<button>').text('Print').addClass('btn btn-primary');
			printButton.on('click', function() {
				window.print();
			});
			$('.page-actions').empty().append(printButton);
        }
    });
	var printStyle = $('<style>').text('@media print { .page-actions, .page-body > div:first-child { display: none; } .company-filter-area { display: none; } }');
    $('head').append(printStyle);
    // Hide the specific div
    // $(wrapper).find('.row.flex.align-center.page-head-content.justify-between').hide();
}
