from odoo import api, fields, models, _


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

    @api.onchange('partner_id', 'payment_term_id')
    def onchange_payment_term(self):
        if self.payment_term_id == self.company_id.mtiba_payment_term_id and self.partner_id:
            if not self.partner_id.ref:
                warning = {
                    'title': _('Warning!'),
                    'message': _('Please add Mtiba reference number on customer card.'),
                }
                return {
                    'warning': warning
                }
            else:
                response = self.env['mtiba']._do_request('/patient', params={'q': self.partner_id.ref}, type='GET')
                if response.get('results'):
                    uuid = response['results'][0].get('uuid')
                    if uuid:
                        response = self.env['mtiba']._do_request('/obs', \
                            params = {
                                'patient': uuid,
                                'concept': 'f06a9c94-d1f8-4cce-9799-6c8db991e66d',
                                'limit': 1,
                                'startIndex': 0,
                                'v': 'default'
                            }, type='GET')
                        if response.get('results'):
                            self.update({
                                'treatment_code': response.get('results')[0].get('value')
                            })
                            return
        else:
            self.update({
                'treatment_code': None,
            })
            return
