from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    mtiba_username_get = fields.Char('Mtiba Username (GET)')
    mtiba_password_get = fields.Char('Mtiba Password (GET)')
    mtiba_username = fields.Char('Mtiba Username')
    mtiba_password = fields.Char('Mtiba Password')
    mtiba_payment_term_id = fields.Many2one('account.payment.term', string='Mtiba Payment Term')
    mtiba_token = fields.Char('Token')
