# -*- coding: utf-8 -*-
##############################################################################
{
    'name': 'Asset Move',
    'version': '0.1',
    'category': 'Asset',
    'description': """
Manage Asset Move    """,
    'author': 'Tubagus Suhendra (tubagus.suhendra08@gmail.com)',
    'website': 'https://www.defasys.com',
    'depends': ['asset','product','hr','stock','asset_ext'],
    'data': ['security/ir.model.access.csv',
             'views/asset_move_view.xml',
             'views/asset_move_sequence_view.xml',
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
