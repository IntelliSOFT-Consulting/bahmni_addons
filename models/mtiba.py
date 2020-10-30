import ast
import json
import requests
import werkzeug

from requests.exceptions import ConnectionError

from odoo import api, models, _
from odoo.exceptions import AccessError, ValidationError

TIMEOUT = 20


class Mtiba(models.AbstractModel):
    _name = 'mtiba'

    @api.model
    def _do_request(self, uri, params={}, headers={}, type='POST'):
        preuri = self.env['ir.config_parameter'].get_param('mtiba.base.url')
        try:
            if type.upper() == 'GET':
                pass
            elif type.upper() == 'POST':
                r = requests.post(preuri + uri, data=json.dumps(params), headers=headers)
            response = ast.literal_eval(werkzeug.utils.unescape(r.content.decode()).replace('null', '\"null\"'))
            if response.get('status') == 403:
                self._set_token(uri, params=params, headers=headers, type=type)
                headers['Authorization'] = 'Bearer {token}'.format(token=self.env.user.company_id.mtiba_token)
                return self._do_request(uri, params=params, headers=headers, type=type)
        except ConnectionError as e:
            raise AccessError(_('Unable to connect.'))
        return response

    @api.model
    def _set_token(self, uri, params={}, headers={}, type='POST'):
        mtiba_username = self.env.user.company_id.mtiba_username
        mtiba_password = self.env.user.company_id.mtiba_password
        param = {'username': mtiba_username, 'password': mtiba_password}
        if not mtiba_username or not mtiba_password:
            raise ValidationError(_('Please configure Mtiba credentials under Invoicing >> Configuration >> Settings.'))
        response = self._do_request('/auth/accessToken', params=param, headers={'Content-Type': 'application/json'})
        self.env.user.company_id.write({'mtiba_token': response.get('accessToken')})
