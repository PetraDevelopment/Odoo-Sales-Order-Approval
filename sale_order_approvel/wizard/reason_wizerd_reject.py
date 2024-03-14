from odoo import models, fields, api


class RejectReasonWizard(models.TransientModel):
    _name = 'reject.reason.wizard'

    reason_reject = fields.Text(
        string='Quotation Rejection Reason', required=True)
    reason_id = fields.Many2one('quotation.reject.reason')
    sequnce = fields.Char()

    def action_reject_quotation(self):
        print("inside reject quotation")

        reject_reason = self.env['quotation.reject.reason'].create({
            'reason': self.reason_reject,
            # Accessing default_name from context
            'name': self.env.context.get('default_name')
        })

    # return {
    #     'name': 'Select Quotation Reject Reason',
    #     'type': 'ir.actions.act_window',
    #     'view_mode': 'form',

    #     'target': 'new',
    #     'context': {}
     # Create or update a record in quotation.reject.reason
        # self.reason_id.reason = self.reason_reject
    # }
