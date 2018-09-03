from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class report_account_budget(osv.osv_memory):
    _name = "report.account.budget"
    _description = "Budget Statistics"
    _order = 'period, general_budget_id, analytic_account_id' 
    
    _columns = {
        'period': fields.char('Period', size=24, readonly=True, select=True),
        'crossovered_budget_id': fields.many2one('crossovered.budget', 'Budget Name', readonly=True),
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account', select=True),
        'general_budget_id': fields.many2one('account.budget.post', 'Budgetary Position', readonly=True, select=True),
        'planned_amount':fields.float('Planned Amount', readonly=True, digits_compute=dp.get_precision('Account')),
        'reserved_amount':fields.float('Reserved Amount', readonly=True, digits_compute=dp.get_precision('Account')),
        'remaining_amount':fields.float('Remaining Amount', readonly=True, digits_compute=dp.get_precision('Account')),
        'practical_amount':fields.float('Actual Amount', readonly=True, digits_compute=dp.get_precision('Account')),
        'theoritical_amount':fields.float('Theoritical Amount', readonly=True, digits_compute=dp.get_precision('Account')),
        'percentage':fields.float('Percentage (%)', readonly=True, digits_compute=dp.get_precision('Account')),
        'state' : fields.selection([('draft', 'Draft'), 
                                    ('cancel', 'Cancelled'), 
                                    ('confirm', 'Confirmed'), 
                                    ('validate', 'Validated'), 
                                    ('done', 'Done')], 'Status', select=True, required=True, readonly=True),
    }
        
class wizard_account_budget(osv.osv_memory):
    _name = "wizard.account.budget"
    _description = "Wizard Budget Statistics"
    
    _columns = {
        'budget_ids': fields.many2many('crossovered.budget', string='Budget Name'),
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account'),
        'date_from': fields.date('Start Date'),
        'date_to': fields.date('End Date'),
        'general_budget_id': fields.many2one('account.budget.post', 'Budgetary Position'),
        'state': fields.selection([('all', 'All Budget Lines'), 
                                   ('not_draft', 'Confirmed and Approved')], 'Budget Line Status', required=True,
                                  help='Note that canceled budget lines will not displayed')
    }
    
    _defaults = {  
        'state': 'all',  
    }
    
    def view_budget(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids)
        line_obj = self.pool.get('crossovered.budget.lines')
        cr.execute('TRUNCATE report_account_budget')
        dom = []
        
        if wizard.budget_ids:
            dom.append(('crossovered_budget_id', 'in', wizard.budget_ids.ids))
        if wizard.analytic_account_id:
            dom.append(('analytic_account_id', '=', wizard.analytic_account_id.id))
        if wizard.general_budget_id:
            dom.append(('general_budget_id', '=', wizard.general_budget_id.id))
        if wizard.date_to:
            dom.append(('date_to', '<=', wizard.date_to))
        if wizard.date_from:
            dom.append(('date_from', '>=', wizard.date_from))
        state = ['confirm', 'validate', 'done']
        if wizard.state == 'all':
            state.append('draft')
        dom.append(('state', 'in', state))
        
        line_ids = line_obj.search(cr, uid, dom)
        if not line_ids:
            raise osv.except_osv(_('Warning!'), _("No Budget Line Found!"))
        
        line_recs = line_obj.browse(cr, uid, line_ids)
        
        column = '(period, crossovered_budget_id, analytic_account_id, general_budget_id, \
                    planned_amount, reserved_amount, remaining_amount, practical_amount, \
                    theoritical_amount, percentage, state)'
        values = ''
        for line in line_recs:
            values += '('
            values += "'" + line.date_from + ' to ' + line.date_to + "', "
            values += '%s, %s, %s, %s, %s, %s, %s, %s, %s, ' % (line.crossovered_budget_id.id, \
                                                                line.analytic_account_id.id, \
                                                                line.general_budget_id.id, \
                                                                line.planned_amount, \
                                                                line.reserved_amount, \
                                                                line.remaining_amount, \
                                                                line.practical_amount, \
                                                                line.theoritical_amount, \
                                                                line.percentage)
            values += "'" + line.state + "'" + '), '
        cr.execute("INSERT INTO report_account_budget %s VALUES %s" % (column, values[:-2]))
        return {
            'name': _('Budget Report'),
            'view_mode': 'graph',
            'view_type': 'form',
            'context': {'graph_view_ref': 'account_reserved_budget.view_account_budget_graph',
                        'search_view_ref': 'account_reserved_budget.view_crossovered_budget_line_search',
                        },
            'res_model': 'report.account.budget',
            'type': 'ir.actions.act_window',
        }
        