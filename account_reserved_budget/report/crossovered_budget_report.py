# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import time
from openerp.osv import osv
from openerp.report import report_sxw
from openerp.addons.account_budget.report.crossovered_budget_report import budget_report as br


class budget_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(budget_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'funct': self.funct,
            'funct_total': self.funct_total,
            'time': time,
        })
        self.context = context

    def funct(self, object, form, ids=None, done=None, level=1):
        global tot
        tot = {
            'theo':0.00,
            'pln':0.00,
            'res':0.00,
            'rem':0.00,
            'prac':0.00,
            'perc':0.00
        }
        result = []

        budget_id = self.pool.get('crossovered.budget').browse(self.cr, self.uid, object.id, self.context.copy())
        d_from = form['date_from']
        d_to = form['date_to']
        
        sum_data = {}
        for line in budget_id.crossovered_budget_line:
            if line.date_from < d_from and line.date_to > d_to:
                continue
            if not line.analytic_account_id:
                continue
            if not sum_data.get(line.analytic_account_id.id, False) :
                sum_data[line.analytic_account_id.id] = {
                    'b_id': -1,
                    'a_id': -1,
                    'name': line.analytic_account_id.name,
                    'status': 1,
                    'theo': line.theoritical_amount,
                    'pln': line.planned_amount,
                    'res' : line.reserved_amount,
                    'rem' : line.remaining_amount,
                    'prac': line.practical_amount,
                    'full' : {}
                }
            else :
                sum_data[line.analytic_account_id.id]['theo'] += line.theoritical_amount
                sum_data[line.analytic_account_id.id]['pln'] += line.planned_amount
                sum_data[line.analytic_account_id.id]['res'] += line.reserved_amount
                sum_data[line.analytic_account_id.id]['rem'] += line.remaining_amount
                sum_data[line.analytic_account_id.id]['prac'] += line.practical_amount
            if not sum_data[line.analytic_account_id.id]['full'].get(line.general_budget_id.id, False):
                sum_data[line.analytic_account_id.id]['full'][line.general_budget_id.id]={
                    'b_id': line.general_budget_id.id,
                    'a_id': line.analytic_account_id.id,
                    'name': line.general_budget_id.name,
                    'status': 2,
                    'theo': line.theoritical_amount,
                    'pln': line.planned_amount,
                    'res' : line.reserved_amount,
                    'rem' : line.remaining_amount,
                    'prac': line.practical_amount,
                }
            else:
                sum_data[line.analytic_account_id.id]['full'][line.general_budget_id.id]['theo'] += line.theoritical_amount
                sum_data[line.analytic_account_id.id]['full'][line.general_budget_id.id]['pln'] += line.planned_amount
                sum_data[line.analytic_account_id.id]['full'][line.general_budget_id.id]['res'] += line.reserved_amount
                sum_data[line.analytic_account_id.id]['full'][line.general_budget_id.id]['rem'] += line.remaining_amount
                sum_data[line.analytic_account_id.id]['full'][line.general_budget_id.id]['prac'] += line.practical_amount
            tot['theo'] += line.theoritical_amount
            tot['pln'] += line.planned_amount
            tot['res'] += line.reserved_amount
            tot['rem'] += line.remaining_amount
            tot['prac'] += line.practical_amount
        for an_acc_id in sum_data:
            temp = sum_data[an_acc_id]['full']
            sum_data[an_acc_id].pop('full', None)
            sum_data[an_acc_id]['perc'] = sum_data[an_acc_id]['theo'] == 0.0 and 0.0 or \
                                            sum_data[an_acc_id]['prac'] / sum_data[an_acc_id]['theo'] * 100
            result.append(sum_data[an_acc_id])
            if not form['report'] == 'analytic-full':
                continue
            for gen_budget_id in temp:
                temp[gen_budget_id]['perc'] = temp[gen_budget_id]['theo'] == 0.0 and 0.0 or \
                                                temp[gen_budget_id]['prac'] / temp[gen_budget_id]['theo'] * 100
                result.append(temp[gen_budget_id])
        return result

    def funct_total(self, form):
        tot['perc'] = tot['theo'] == 0.00 and 0.00 or tot['prac'] / tot['theo'] * 100
        return [{
             'tot_theo': tot['theo'],
             'tot_pln': tot['pln'],
             'tot_res': tot['res'],
             'tot_rem': tot['rem'],
             'tot_prac': tot['prac'],
             'tot_perc': tot['perc']
        }]

class report_crossoveredbudget(osv.AbstractModel):
    _name = 'report.account_reserved_budget.report_crossoveredbudget'
    _inherit = 'report.abstract_report'
    _template = 'account_reserved_budget.report_crossoveredbudget'
    _wrapped_report_class = budget_report

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
