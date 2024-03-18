from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError  # Import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _rec_name = 'ref'

    state = fields.Selection(
        selection_add=[

            ('waiting_for_verify', 'WAITING FOR VERIFY'),
            ('waiting_for_approval', 'APPROVAL')
        ], readonly=True, index=True, copy=False, track_visibility='onchange'
    )

    # check = fields.Char(default='check approve', readonly=True)

    ref = fields.Char(compute="_set_record_name", store=False)

    @api.depends('name', 'state')
    def _set_record_name(self):
        for sale_order in self:
            if sale_order.state in ['draft', 'waiting_for_verify', 'waiting_for_approval', 'sale', 'cancel']:
                # Remove existing state labels from the name
                name_without_state = sale_order.name.split('(')[0].strip()
                # Append the state label to the name
                if sale_order.state == 'draft':
                    sale_order.ref = name_without_state + '(draft)'
                elif sale_order.state == 'waiting_for_verify':
                    sale_order.ref = name_without_state + \
                        '(WAITING FOR VERIFY)'
                elif sale_order.state == 'waiting_for_approval':
                    sale_order.ref = name_without_state + \
                        '(APPROVAL)'
                elif sale_order.state == 'sale':
                    sale_order.ref = name_without_state + '(sale)'
                elif sale_order.state == 'cancel':
                    sale_order.ref = name_without_state + '(cancel)'

    def submit_for_verify(self):
        for rec in self:
            print("Inside waiting for verify action")
            rec.state = 'waiting_for_verify'

    def submit_for_approval(self):
        for rec in self:
            print("Inside WAITING FOR APPROVAL action")
            rec.state = 'waiting_for_approval'
        return {

        }
    reject_reason = fields.Char(string="Reject Reason", tracking=3)

    def action_reject_quotation_wizard(self):
        print('action wizard')

        # Get the default reason_reject from the context
        # default_reason_reject = self._context.get('default_reason_reject', '')

        # # Store the default_reason_reject in reasonin_sale field
        # self.reasonin_sale = default_reason_reject
        # print("reasonin_sale == ", default_reason_reject)
        return {

            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'reject.reason.wizard',
            'target': 'new',
            'context': {
                'default_reason_reject': '',
                'default_name': self.name,
				'default_sale_order_id': self.id
            },
        }

    def reject_approve(self):
        action = self.action_reject_quotation_wizard()
        return action

    def action_cancel(self):
        # Override the action_cancel method to perform additional actions
        for order in self:
            order.state = 'cancel'
        return super(SaleOrder, self).action_cancel()

    def _can_be_confirmed(self):
        self.ensure_one()
        return self.state in {'draft', 'sent', 'waiting_for_approval'}

    def action_confirm(self):
        # Check if any of the orders can be confirmed
        if not self._can_be_confirmed():
            # Raise a UserError if no orders can be confirmed
            raise UserError(_("The following orders are not in a state requiring confirmation: %s" % ", ".join(
                self.filtered(lambda order: not order._can_be_confirmed()).mapped('name'))))

        # Call the superclass method to confirm the sale orders
        return super(SaleOrder, self).action_confirm()

        # return {
        #     'name': 'Select Quotation Reject Reason',
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form', }

    # def reject_approve(self):
    #     for rec in self:
    #         print("Inside draft action")
    #         rec.state = 'draft'
  # @api.constrains('state', 'paid_amount2', 'payment_term_id')
    # def _check_paid_amount_required(self):
    #     for order in self:
    #         # Check if the order state is 'waiting_for_verify' and both 'paid_amount2' and 'payment_term_id' are not set
    #         if order.state == 'waiting_for_verify' and (not order.paid_amount2 or not order.payment_term_id):
    #             raise ValidationError(
    #                 _("Paid Amount and Payment Term are required before verifying the order."))
    # state = fields.Selection(
    #     selection_add=[

    #         ('waiting_for_verify', 'WAITING FOR VERIFY'),
    #         ('waiting_for_approval', 'WAITING FOR APPROVAL')
    #     ], readonly=True, index=True, copy=False, track_visibility='onchange'
    # )
