frappe.ui.form.on('Exit Interview', {
	refresh:function(frm) {
		frm.set_value('ref_doctype', 'Exit Questionnaire');
		frm.refresh_field('ref_doctype');
	},
    employee: function(frm){
        frm.set_query("reference_document_name",function(){
            return{
                filters:{
                    'employee':cur_frm.doc.employee
                }
                
            };
        });
    }
});