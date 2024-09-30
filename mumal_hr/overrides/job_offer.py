# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, flt, get_link_to_form

from hrms.hr.doctype.job_offer.job_offer import JobOffer as Document

class CustomJobOffer(Document):
	def on_change(self):
		# Overriding the on_change method; custom logic can be added here
		pass

	