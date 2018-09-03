# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class account_financial_report(osv.osv):
    _inherit = "account.financial.report"

    _columns = {
        'show_amount': fields.boolean("Show Amount"),
    }
    
    _defaults = {
        'show_amount': True
    }