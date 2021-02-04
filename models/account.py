import datetime
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    treatment_code = fields.Char('Treatment Code')
    mtiba_transaction_identity = fields.Char('Mtiba Transaction ID', readonly=True)

    @api.multi
    def invoice_validate(self):
        for invoice in self:
            if invoice.treatment_code:
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
                    'diagnosis': [
                        {
                          'scheme': 'SCM123',
                          'code': 'A001',
                          'description': 'General',
                        }
                    ],
                    'notes': 'Doctors notes',
                }
                for line in invoice.invoice_line_ids:
                    params['invoice']['items'].append({
                        'scheme': 'SCM123',
                        'code': line.product_id.default_code or '',
                        'description': line.name,
                        'price': {
                            'currency': invoice.currency_id.name,
                            'amount': line.price_unit,
                        },
                        'quantity': line.quantity,
                        'category': line.product_id.categ_id.name,
                        'status': 'SUBMITTED',
                        'externalCode': '',
                    })
                _logger.info('Invoice {name}: Payload - {payload}'.format(name=invoice.number, payload=params))
                response = self.env['mtiba']._do_request('/invoices/{treatment_code}?action=Submit'.format(treatment_code=invoice.treatment_code), params=params, headers=headers)
                if response.get('id'):
                    invoice.write({'mtiba_transaction_identity': str(response['id'])})
                else:
                    raise ValidationError(_('Unable to register invoice. {msg}'.format(msg=response.get('message', ''))))
                _logger.info('Response from invoice {name} submission action: {resp}'.format(name=invoice.number, resp=response))
        return super(AccountInvoice, self).invoice_validate()
