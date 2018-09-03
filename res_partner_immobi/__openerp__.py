# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Res Partner IMMOBI',
    'version' : '1.1',
    'summary': 'Res Partner IMMOBI',
    'description': """
        Res Partner IMMOBI
    """,
    'category' : 'purchase',
    'author': 'Taufik',
    'website': '',
    'depends' : ['base','account','purchase'],
    'data': [   
             'security/ir.model.access.csv',
             'res_partner_code_view.xml'
             ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
}
