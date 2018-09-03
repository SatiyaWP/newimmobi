# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Accounting Reporting XLS',
    'version' : '8.1.0',
    'summary': 'Accounting Reporting to XLS',
    'description': """
        Financial (P&L/BS) Report XLS.
        """,
    'author': 'Joenan. Email: joenannr@gmail.com',
    'website': 'https://keepapp.co.id/',
    'depends' : ['account'],
    'data': [
             'views/account_financial_report_view.xml',
             'wizard/accounting_report_view.xml'
             ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
}
