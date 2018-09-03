# -*- coding:utf-8 -*-

{
    'name': 'Payroll BPJS',
    'version': '1.0',
    'category': 'Generic Modules/Human Resources',
    'author': "Ido <indro.prihatno@gmail.com>,"
              "Odoo Community Association (OCA)",
    'website': 'http://www.openerp.com',
    'license': 'AGPL-3',
    'depends': [
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_bpjs.xml',
    ],
    'test': [
    ],
    'installable': True,
}
