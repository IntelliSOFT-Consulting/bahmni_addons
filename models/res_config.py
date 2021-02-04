from odoo import api, fields, models


class CalendarSettings(models.TransientModel):

    _inherit = 'account.config.settings'

    mtiba_username_get = fields.Char('Mtiba Username (GET)')
    mtiba_password_get = fields.Char('Mtiba Password (GET)')
    mtiba_username = fields.Char('Mtiba Username')
    mtiba_password = fields.Char('Mtiba Password')
    mtiba_payment_term_id = fields.Many2one('account.payment.term', string='Mtiba Payment Term')

    @api.multi
    def set_mtiba_credentials(self):
        if self.mtiba_username_get and self.mtiba_username_get != self.company_id.mtiba_username_get:
            self.company_id.write({'mtiba_username_get': self.mtiba_username_get})
        if self.mtiba_password_get and self.mtiba_password_get != self.company_id.mtiba_password_get:
            self.company_id.write({'mtiba_password_get': self.mtiba_password_get})
        if self.mtiba_username and self.mtiba_username != self.company_id.mtiba_username:
            self.company_id.write({'mtiba_username': self.mtiba_username})
        if self.mtiba_password and self.mtiba_password != self.company_id.mtiba_password:
            self.company_id.write({'mtiba_password': self.mtiba_password})
        if self.mtiba_payment_term_id and self.mtiba_payment_term_id != self.company_id.mtiba_payment_term_id:
            self.company_id.write({'mtiba_payment_term_id': self.mtiba_payment_term_id.id})

    def get_default_mtiba_credentials(self, fields):
        company = self.env.user.company_id
        return dict(
            mtiba_username_get=company.mtiba_username_get,
            mtiba_password_get=company.mtiba_password_get,
            mtiba_username=company.mtiba_username,
            mtiba_password=company.mtiba_password,
            mtiba_payment_term_id=company.mtiba_payment_term_id.id
        )
