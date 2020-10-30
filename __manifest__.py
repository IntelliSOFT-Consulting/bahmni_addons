# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bahmni Mtiba Integration',
    'version': '10.0',
    'category': 'Payment',
    'depends': ['sale'],
    'data': [
        'data/ir_config_parameter_data.xml',
        'views/account_invoice_view.xml',
        'views/res_config_views.xml',
        'views/sale_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
