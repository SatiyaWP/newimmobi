# -*- coding: utf-8 -*-

from openerp.osv import osv, fields

class account_account(osv.osv):
    _inherit = "account.account"

    _columns = {
        "is_consolidation": fields.boolean("Consolidation", help="For consolidation report"),
        "is_elimination": fields.boolean("Elimination", help="For consolidation report")
    }
