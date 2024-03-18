from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _rec_name = 'ref'

    state = fields.Selection(
        selection_add=[
            ('waiting_for_verify', 'WAITING FOR VERIFY'),
            ('waiting_for_approval', 'APPROVAL')], readonly=True, index=True, copy=False, track_visibility='onchange'
    )

    # check = fields.Char(default='check approve', readonly=True)

    ref = fields.Char(compute="_set_record_name", store=True)

    @api.depends('name', 'state')
    def _set_record_name(self):
        for sale_order in self:
            if sale_order.state in ['draft', 'waiting_for_verify', 'waiting_for_approval', 'sale', 'cancel']:
                # Print out the values of 'name' and 'state'
                print("Name:", sale_order.name)
                print("State:", sale_order.state)

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
    reasonin_sale = fields.Char(tracking=True)

    def reject_approve(self):
        action = self.action_reject_quotation_wizard()
        return action

    def action_cancel(self):
        # Override the action_cancel method to perform additional actions
        for order in self:
            order.state = 'cancel'
        return super(SaleOrder, self).action_cancel()
