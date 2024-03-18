
from odoo import fields, models, api
from odoo.exceptions import UserError


class QuotationRejectReason(models.Model):
    _name = 'quotation.reject.reason'
    _description = 'quotation_reject_reason'
    _inherit = "mail.thread"

    reason = fields.Char(string='Reject Reason')
    name = fields.Char(string='Number')
