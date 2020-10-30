from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    treatment_code = fields.Char('Treatment Code')

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(SaleOrder, self).onchange_partner_id()
        values = {'payment_term_id': self.env.user.company_id.mtiba_payment_term_id.id}
        self.update(values)
        return res

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        res = super(SaleOrder, self).action_invoice_create(grouped=grouped, final=final)
        invoice = self.env['account.invoice']
        for order in self:
            for invoice_id in res:
                if invoice_id in order.invoice_ids.ids:
                    invoice.browse(invoice_id).write({'treatment_code': order.treatment_code})
        return res
