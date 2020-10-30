import datetime
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    treatment_code = fields.Char('Treatment Code')

    @api.multi
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()
        for invoice in self:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {token}'.format(token=self.env.user.company_id.mtiba_token or '')}
            params = {
                'invoice': {
                    'treatmentCode': invoice.treatment_code,
                    'externalTreatmentCode': '',
                    'createdBy': invoice.create_uid.name,
                    'createdOn': datetime.datetime.strptime(invoice.create_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'),
                    'items': [],
                },
                'payments': [
                    {
                        'type': 'Benefit',
                        'total': {
                            'currency': invoice.currency_id.name,
                            'amount': invoice.amount_total,
                        }
                    },
                    {
                        'type': 'Cash',
                        'total': {
                            'currency': invoice.currency_id.name,
                            'amount': 0,
                        }
                    },
                ],
            }
            for line in invoice.invoice_line_ids:
                params['invoice']['items'].append({
                    'scheme': 'SCM123',
                    'code': line.product_id.default_code or '',
                    'description': line.name,
                    'price': {
                        'currency': invoice.currency_id.name,
                        'amount': line.price_subtotal,
                    },
                    'quantity': line.quantity,
                    'category': line.product_id.categ_id.name,
                    'status': 'SUBMITTED',
                    'externalCode': '',
                })
            _logger.info('Invoice {name}: Payload - {payload}'.format(name=invoice.number, payload=params))
            response = self.env['mtiba']._do_request('/invoices/{treatment_code}?action=Submit'.format(treatment_code=invoice.treatment_code), params=params, headers=headers)
            invoice.message_post(body='Mtiba Response: {msg}'.format(msg=response.get('message')))
            _logger.info('Invoice {name}: Response - {mtiba_response}'.format(name=invoice.number, mtiba_response=response.content))
        return res
