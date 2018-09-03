# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.report import report_sxw
from common_report_header import common_report_header

class report_account_common(report_sxw.rml_parse, common_report_header):

    def __init__(self, cr, uid, name, context=None):
        super(report_account_common, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_lines': self.get_lines,
            'time': time,
            'get_fiscalyear': self._get_fiscalyear,
            'get_account': self._get_account,
            'get_start_period': self.get_start_period,
            'get_end_period': self.get_end_period,
            'get_filter': self._get_filter,
            'get_start_date':self._get_start_date,
            'get_end_date':self._get_end_date,
            'get_target_move': self._get_target_move,
        })
        self.context = context

class AccountingReport(osv.osv_memory):
    _inherit = "accounting.report"
    
    def _get_additional_level(self, report):
        add_level = -1
        while report.parent_id:
            report = report.parent_id
            add_level += 1
        return add_level

    def set_context(self, objects, data, ids, report_type=None):
        new_ids = ids
        if (data['model'] == 'ir.ui.menu'):
            new_ids = 'chart_account_id' in data['form'] and [data['form']['chart_account_id']] or []
            objects = self.pool.get('account.account').browse(cr, uid, new_ids)
        return super(report_account_common, self).set_context(objects, data, new_ids, report_type=report_type)

    def get_lines(self, cr, uid, ids, data, context=None):
        lines = []
        account_obj = self.pool.get('account.account')
        currency_obj = self.pool.get('res.currency')
        ids2 = self.pool.get('account.financial.report')._get_children_by_order(cr, uid, [data['form']['account_report_id'][0]], context=data['form']['used_context'])
        for report in self.pool.get('account.financial.report').browse(cr, uid, ids2, context=data['form']['used_context']):
            if not report.parent_id:
                continue 
            vals = {
                'name': report.name,
#                 'balance': report.balance * report.sign or 0.0,
                'type': 'report',
                'level': bool(report.style_overwrite) and report.style_overwrite or report.level,
                'header': True,
                'account_type': report.type == 'sum' and 'view' or False,  # used to underline the financial report balances
                'report_type': report.type
            }
            if report.show_amount:
                # add financial report child balance to its parent
                child_balance, child_debit, child_credit, child_balance_cmp = 0.0, 0.0, 0.0, 0.0
                if report._get_children_by_order():
                    for report_child in self.pool.get('account.financial.report').browse(cr, uid, report._get_children_by_order()):
                        if report_child.type == 'account_report' and report_child.parent_id == report:
                            child_balance += report_child.balance * report_child.sign
                            child_debit += report_child.debit
                            child_credit += report_child.credit
                            child_balance_cmp += self.pool.get('account.financial.report').browse(cr, uid, report_child.id, context=data['form']['comparison_context']).balance * report_child.sign
                
                vals['balance'] = report.balance * report.sign + child_balance or 0.0
                if data['form']['debit_credit'] or self.pool.get('account.account').browse(cr, uid, data['form']['chart_account_id']).is_elimination:
                    vals['debit'] = report.debit + child_debit
                    vals['credit'] = report.credit + child_credit
                if data['form']['enable_filter']:
                    vals['balance_cmp'] = self.pool.get('account.financial.report').browse(cr, uid, report.id, context=data['form']['comparison_context']).balance * report.sign + child_balance_cmp or 0.0
            lines.append(vals)
            account_ids = []
            if report.display_detail == 'no_detail':
                # the rest of the loop is used to display the details of the financial report, so it's not needed here.
                continue
            if report.type == 'accounts' and report.account_ids:
                account_ids = account_obj._get_children_and_consol(cr, uid, [x.id for x in report.account_ids])
            elif report.type == 'account_type' and report.account_type_ids:
                account_ids = account_obj.search(cr, uid, [('user_type', 'in', [x.id for x in report.account_type_ids])])
            if account_ids:
                for account in account_obj.browse(cr, uid, account_ids, context=data['form']['used_context']):
                    # if there are accounts to display, we add them to the lines with a level equals to their level in
                    # the COA + 1 (to avoid having them with a too low level that would conflicts with the level of data
                    # financial reports for Assets, liabilities...)
                    if report.display_detail == 'detail_flat' and account.type == 'view':
                        continue
                    flag = False
                    vals = {
                        'name': account.name,
                        'balance':  account.balance != 0 and account.balance * report.sign or account.balance,
                        'type': 'account',
                        'level': report.display_detail == 'detail_with_hierarchy' and min(account.level + 1, 6) + self._get_additional_level(report) or 6,  # account.level + 1
                        'header': account.child_parent_ids and True or False,
                        'account_type': account.type,
                    }

                    if data['form']['debit_credit']:
                        vals['debit'] = account.debit
                        vals['credit'] = account.credit
                    if not currency_obj.is_zero(cr, uid, account.company_id.currency_id, vals['balance']):
                        flag = True
                    if data['form']['enable_filter']:
                        vals['balance_cmp'] = account_obj.browse(cr, uid, account.id, context=data['form']['comparison_context']).balance * report.sign or 0.0
                        if not currency_obj.is_zero(cr, uid, account.company_id.currency_id, vals['balance_cmp']):
                            flag = True
                    if flag:
                        lines.append(vals)
        return lines
    
    def _build_comparison_context(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        result = {}
#         result['fiscalyear'] = 'fiscalyear_id_cmp' in data['form'] and data['form']['fiscalyear_id_cmp'] or False
        result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['chart_account_id'] = 'chart_account_id' in data['form'] and data['form']['chart_account_id'] or False
        result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
        if data['form']['filter_cmp'] == 'filter_date':
            result['date_from'] = data['form'].get('date_from_cmp', False)
            result['date_to'] = data['form']['date_to_cmp']
        elif data['form']['filter_cmp'] == 'filter_period':
            if not data['form']['period_to_cmp']:
                raise osv.except_osv(_('Error!'), _('Select the ending period'))
            result['period_from'] = data['form'].get('period_from_cmp', False)
            result['period_to'] = data['form']['period_to_cmp']
        return result
    
    def _build_contexts(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        result = {}
#         result['fiscalyear'] = 'fiscalyear_id' in data['form'] and data['form']['fiscalyear_id'] or False
        result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['chart_account_id'] = 'chart_account_id' in data['form'] and data['form']['chart_account_id'] or False
        result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
        if data['form']['filter'] == 'filter_date':
            result['date_from'] = data['form']['date_from']
            result['date_to'] = data['form']['date_to']
        elif data['form']['filter'] == 'filter_period':
            if not data['form']['period_to']:
                raise osv.except_osv(_('Error!'),_('Select the ending period.'))
            result['period_from'] = data['form']['period_from']
            result['period_to'] = data['form']['period_to']
        return result
    
    def _print_report(self, cr, uid, ids, data, context=None):
        account_obj = self.pool.get('account.account')
        data['form'].update(self.read(cr, uid, ids, ['period_from_cmp', 'period_to_cmp', 'date_from_cmp', 'debit_credit', 'date_to_cmp', 'filter_cmp', 'account_report_id', 'enable_filter', 'label_filter', 'target_move'])[0])
        data['form']['period_from_cmp'] = self.browse(cr, uid, ids).period_from_cmp.id
        data['form']['period_to_cmp'] = self.browse(cr, uid, ids).period_to_cmp.id
        data['form']['fiscalyear_id_cmp'] = self.browse(cr, uid, ids).fiscalyear_id_cmp.id
        if context['xls_export']:
            if context.get('consolidation', False):
#                 cr.execute("select id, coalesce(is_consolidation,False) as is_consolidation, code, name from account_account where parent_id is null order by id")
#                 coa = cr.fetchall()
                coa_ids = account_obj.search(cr, uid, [('parent_id', '=', False)])
                coa = []
                for coa_id in coa_ids:
                    if account_obj.browse(cr, uid, coa_id).is_consolidation:
                        coa.append([coa_id, True, account_obj.browse(cr, uid, coa_id).code, account_obj.browse(cr, uid, coa_id).name, account_obj.browse(cr, uid, coa_id).is_elimination])
                    else:
                        coa.append([coa_id, False, account_obj.browse(cr, uid, coa_id).code, account_obj.browse(cr, uid, coa_id).name, account_obj.browse(cr, uid, coa_id).is_elimination])
            else:
                coa = [[data['form']['chart_account_id'], False, account_obj.browse(cr, uid, data['form']['chart_account_id']).code, account_obj.browse(cr, uid, data['form']['chart_account_id']).name, account_obj.browse(cr, uid, data['form']['chart_account_id']).is_elimination]]
            finance = self.browse(cr, uid, ids, context)
            # we update form with display account value
            datas = {}
            datas['name'] = finance.account_report_id.name
            datas['company_id'] = finance.company_id.name
            datas['currency_id'] = finance.company_id.currency_id.name
            data['form']['chart_account_id'] = 0
            datas['data'] = []
            for coa_id in coa:
                if coa_id[1]:
                    continue
                data['form']['chart_account_id'] = data['form']['used_context']['chart_account_id'] = coa_id[0]
                data['form'].update({'comparison_context':self._build_comparison_context(cr, uid, ids, data, context)})
#                 datas['data'].append([{"coa_code":coa_id[2],"coa_name":coa_id[3]}] + self.get_lines(cr,uid, ids, data, context))
                array = []
                array.append([{"coa_code":coa_id[2], "coa_name":coa_id[3], "elimination":coa_id[4]}])
                array.append(self.get_lines(cr, uid, ids, data, context))
                datas['data'].append(array)
            # for consolidation coa
            for coa_id in coa:
                if coa_id[1]:
                    data['form']['chart_account_id'] = data['form']['used_context']['chart_account_id'] = coa_id[0]
                    data['form'].update({'comparison_context':self._build_comparison_context(cr, uid, ids, data, context)})
                    array = []
                    array.append([{"coa_code":coa_id[2], "coa_name":coa_id[3], "elimination":coa_id[4]}])
                    array.append(self.get_lines(cr, uid, ids, data, context))
                    datas['data'].append(array)
            datas['info'] = data
            datas["info"]["form"].update({"period_from": self.pool["account.period"].browse(cr, uid, datas["info"]["form"]["period_from"]).name, "period_to":self.pool["account.period"].browse(cr, uid, datas["info"]["form"]["period_to"]).name})
            
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'financial_report',
                'nodestroy': False,
                'data': data,
                'datas': datas
            }
            
        else:
            return self.pool['report'].get_action(cr, uid, [], 'account.report_financial', data=data, context=context)

