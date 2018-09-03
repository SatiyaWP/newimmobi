# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2013 Noviat nv/sa (www.noviat.com). All rights reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm
# import logging
# _logger = logging.getLogger(__name__)

class AccountAgedPertnerBalance_xls(orm.TransientModel):
    """Will launch age partner balance report.
    This report is based on Open Invoice Report
    and share a lot of knowledge with him
    """
    
    _inherit = "account.aged.trial.balance.webkit"
    _description = "Aged partner balanced"
    
    def xls_export(self, cr, uid, ids, context=None):
        return self.check_report(cr, uid, ids, context=context)

    def _print_report(self, cr, uid, ids, data, context=None):
        context = context or {}
        aged_partner_wiz = self.browse(cr,uid,ids)
        data['until_date'] = aged_partner_wiz.until_date
        data['target_move'] = aged_partner_wiz.target_move
        data['result_selection'] = aged_partner_wiz.result_selection
        data['chart_account_id'] = aged_partner_wiz.chart_account_id.name
        data['period_to'] = aged_partner_wiz.period_to.name
        
        if context.get('xls_export'):
            # we update form with display account value
            data = self.pre_print_report(cr, uid, ids, data, context=context)
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'account.account_report_aged_partner_balance_xls',
                'nodestroy': True,
                'datas': data,
            }
        else:
            return super(AccountAgedPertnerBalance_xls, self)._print_report(
                cr, uid, ids, data, context=context)
