from odoo import models, fields, api
from odoo.exceptions import UserError  # Import UserError


class RejectReasonWizard(models.TransientModel):
    _name = 'reject.reason.wizard'

    reason_reject = fields.Text(
        string='Quotation Rejection Reason')
    reason_id = fields.Many2one('quotation.reject.reason')
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    sequnce = fields.Char()

    def action_reject_quotation(self):
        print("inside reject quotation")

        # Get the active sale order ID from the context
        active_id = self.env.context.get('active_id')
        sale_order = self.env['sale.order'].browse(active_id)

        if not sale_order:
            raise UserError("Sale order not found.")

        if not self.reason_reject:
            raise UserError(
                "Please provide a reject reason before canceling the order.")

        reject_reason = self.env['quotation.reject.reason'].create({
            'reason': self.reason_reject,
            'name': sale_order.name
        })

        # Call the action_cancel method of the sale order model to change the state to 'cancel'
        sale_order.action_cancel()

        self.sale_order_id.reject_reason = self.reason_reject

        return {'type': 'ir.actions.act_window_close'}

    # return {
    #     'name': 'Select Quotation Reject Reason',
    #     'type': 'ir.actions.act_window',
    #     'view_mode': 'form',

    #     'target': 'new',
    #     'context': {}
     # Create or update a record in quotation.reject.reason
        # self.reason_id.reason = self.reason_reject
    # }
