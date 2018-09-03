# -*- coding: utf-8 -*-
##############################################################################
{
    'name': 'Contract Template',
    'version': '0.1',
    'category': 'HR',
    'description': """
Contract Template    """,
    'author': 'Tubagus Suhendra (tubagus.suhendra08@gmail.com)',
    'website': 'https://www.defasys.com',
    'depends': ['base','hr','hr_contract','hr_payroll'],
    'data': ['security/ir.model.access.csv',
             'views/contract_template_view.xml',
             'views/template_report.xml',
             #'views/asset_move_sequence_view.xml',
    ],
    'test': [
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
