from openerp import api
from openerp.osv import fields, osv, expression
from openerp.tools import ustr
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class account_budget_crossvered_summary_report(osv.osv_memory):

    _inherit = 'account.budget.crossvered.summary.report'
    
    def check_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, context=context)[0]
        datas = {
            'ids': context.get('active_ids',[]),
            'model': 'crossovered.budget',
            'form': data
        }
        datas['form']['ids'] = datas['ids']
        datas['form']['report'] = 'analytic-one'
        return self.pool['report'].get_action(cr, uid, [], 'account_reserved_budget.report_crossoveredbudget', data=datas, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shif
class account_budget_crossvered_report(osv.osv_memory):

    _inherit = "account.budget.crossvered.report"
    
    def check_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, context=context)[0]
        datas = {
            'ids': context.get('active_ids', []),
            'model': 'crossovered.budget',
            'form': data
        }
        datas['form']['ids'] = datas['ids']
        datas['form']['report'] = 'analytic-full'
        return self.pool['report'].get_action(cr, uid, [], 'account_reserved_budget.report_crossoveredbudget', data=datas, context=context)

class crossovered_budget_lines_approve(osv.osv_memory):
    _name = 'crossovered.budget.lines.approve'
    
    def button_validate(self, cr, uid, ids, context=None):
        
        for line in self.pool.get('crossovered.budget.lines').browse(cr, uid, context.get('active_ids', [])):
            if line.state == 'confirm':
                line.button_validate()
            else:
                raise osv.except_osv(_('Warning!'), _("Cannot approve budget not in Confirmed State!"))
            
    def button_confirm(self, cr, uid, ids, context=None):
        
        for line in self.pool.get('crossovered.budget.lines').browse(cr, uid, context.get('active_ids', [])):
            if line.state == 'draft':
                line.button_confirm()
            else:
                raise osv.except_osv(_('Warning!'), _("Cannot confirm budget not in draft State!"))

class account_budget_post(osv.osv):
    _inherit = "account.budget.post"
    
    def name_get(self, cr, uid, ids, context=None):
        res = []
        if not ids:
            return res
        if isinstance(ids, (int, long)):
            ids = [ids]
        for id in ids:
            elmt = self.browse(cr, uid, id, context=context)
            res.append((id,elmt.code + ' ' + elmt.name))
        return res
    
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if operator in expression.NEGATIVE_TERM_OPERATORS:
            domain = [('code', operator, name), ('name', operator, name)]
        else:
            domain = ['|', ('code', operator, name), ('name', operator, name)]
        ids = self.search(cr, user, expression.AND([domain, args]), limit=limit, context=context)
        return self.name_get(cr, user, ids, context=context)
    
class account_analytic_account(osv.osv):
    _inherit = "account.analytic.account"
    _order = "parent_left"
    _parent_order = "code"
    _parent_store = True
        
    _columns = {
        'parent_left': fields.integer('Parent Left', select=1),
        'parent_right': fields.integer('Parent Right', select=1),
    }
#     
    def name_get(self, cr, uid, ids, context=None):
        res = []
        if not ids:
            return res
        if isinstance(ids, (int, long)):
            ids = [ids]
        for id in ids:
            elmt = self.browse(cr, uid, id, context=context)
            res.append((id,elmt.code + ' ' + elmt.name))
        return res
    
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if operator in expression.NEGATIVE_TERM_OPERATORS:
            domain = [('code', operator, name), ('name', operator, name)]
        else:
            domain = ['|', ('code', operator, name), ('name', operator, name)]
        ids = self.search(cr, user, expression.AND([domain, args]), limit=limit, context=context)
        return self.name_get(cr, user, ids, context=context)
    
class crossovered_budget(osv.osv):
    _inherit = "crossovered.budget"
    
    def _total_lines(self, cr, uid, ids, name, args, context=None):
        res={}
        cr.execute('SELECT crossovered_budget_id, count(id) \
                    FROM crossovered_budget_lines  \
                    WHERE crossovered_budget_id IN %s\
                    GROUP BY crossovered_budget_id', (tuple(ids),))
        outs = cr.fetchall()
        for out in outs:
            res[out[0]] = out[1]
        return res
    
    _columns = {
        'total_amount': fields.float('Total Amount', readonly=True),
        'total_lines':fields.function(_total_lines, string='Total Lines', type='float', digits_compute=dp.get_precision('Account')),
        'state' : fields.selection([('draft', 'Draft'), ('cancel', 'Cancelled'), ('confirm', 'Confirmed'), ('validate', 'Validated'), ('done', 'Done'), ('switch', 'Switching')], 'Status', select=True, required=True, readonly=True),
    }
    
    
    def budget_done(self, cr, uid, ids, *args):
        for budget in self.browse(cr, uid, ids):
            budget.crossovered_budget_line.button_done()
        return super(crossovered_budget, self).budget_done(cr, uid, ids, *args)
    
    def budget_switch(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state' : 'switch'})
        
    def budget_view(self, cr, uid, ids, *args):
        mod_obj = self.pool.get('ir.model.data')
        dummy, action_id = tuple(mod_obj.get_object_reference(cr, uid, 'account_reserved_budget', 'action_budget_lines'))
        action = self.pool.get('ir.actions.act_window').read(cr, uid, action_id)

        line_ids = []
        for budget in self.browse(cr, uid, ids):
            line_ids += budget.crossovered_budget_line.ids

        #override the context to get rid of the default filtering on picking type
        action['context'] = {'default_crossovered_budget_id': ids[0]}
        #choose the view_mode accordingly
        action['domain'] = "[('crossovered_budget_id','in', %s)]" % ids
        return action
        
    def budget_validate(self, cr, uid, ids, *args):
        for budget in self.browse(cr, uid, ids):
            total_amount = 0.0
            for line in budget.crossovered_budget_line:
                if budget.state != 'switch':
                    line.button_validate()
                total_amount += line.planned_amount
#                 elif line.state != 'cancel':
#                     raise osv.except_osv(_('Warning !'), _('Unable to Approve budget with unnaproved budget line %s for %s from %s to %s') % (line.analytic_account_id.name, line.general_budget_id.name, line.date_from, line.date_to))
                
#             if budget.state == 'switch'and budget.total_amount > total_amount :
#                 raise osv.except_osv(_('Warning !'), _('New Planned Amount Decreased'))
            
            budget.total_amount = total_amount
                
        return super(crossovered_budget, self).budget_validate(cr, uid, ids, *args)
    
    
    def budget_cancel(self, cr, uid, ids, *args):
        for budget in self.browse(cr, uid, ids):
            budget.crossovered_budget_line.button_cancel()
        return super(crossovered_budget, self).budget_cancel(cr, uid, ids, *args)
    
    def budget_draft(self, cr, uid, ids, *args):
        for budget in self.browse(cr, uid, ids):
            budget.crossovered_budget_line.button_draft()
        return super(crossovered_budget, self).budget_draft(cr, uid, ids, *args)
        
class crossovered_budget_lines(osv.osv):
    _inherit = 'crossovered.budget.lines'
    
    def _prac(self, cr, uid, ids, name, args, context=None):
        res = {}
        result = 0.0
        if context is None: 
            context = {}
        account_obj = self.pool.get('account.account')
        analytic_obj = self.pool.get('account.analytic.account')
        for line in self.browse(cr, uid, ids, context=context):
            acc_ids = [x.id for x in line.general_budget_id.account_ids]
            if not acc_ids:
                raise osv.except_osv(_('Warning!'), _("The Budget '%s' has no accounts!") % ustr(line.general_budget_id.name))
            acc_ids = account_obj._get_children_and_consol(cr, uid, acc_ids, context=context)
            an_acc_ids = analytic_obj.search(cr, uid, [('parent_id', 'child_of', [line.analytic_account_id.id])], context=context)
            date_to = line.date_to
            date_from = line.date_from
            if line.analytic_account_id.id:
                cr.execute("SELECT SUM(amount) FROM account_analytic_line WHERE account_id in %s AND (date "
                       "between to_date(%s,'yyyy-mm-dd') AND to_date(%s,'yyyy-mm-dd')) AND "
                       "general_account_id=ANY(%s)", (tuple(an_acc_ids), date_from, date_to, acc_ids,))
                result = cr.fetchone()[0]
            if result is None:
                result = 0.00
            res[line.id] = result
        return res
    
    @api.multi
    def _act(self, name, args):
        res={}
        req_line_obj = self.env['stock.purchase.requisition.line']
        order_line_obj = self.env['purchase.order.line']
        requests = req_line_obj.search([('budget_line_id', 'in', self.ids),
                             ('product_id.valuation', '=', 'real_time'),
                             ('state', '=', 'approved')])
        order_lines = order_line_obj.search([
                                        ('budget_line_id', 'in', self.ids),
                                        ('order_id.state', 'in', ('approved', 'except_picking', 'except_invoice')),
                                        ('state', '=', 'confirmed')])
        for line in self:
            res[line.id] = 0.0
            for obj in requests:
                if line.id == obj.budget_line_id.id:
                    res[line.id] += obj.reserved_amount
            for obj in order_lines:
                if line.id == obj.budget_line_id.id:
                    res[line.id] += obj.reserved_amount
        return res
    
    def _compute_amount(self, cr, uid, ids, name, args, context=None):
        res = {}
        prac_amount = self._prac(cr, 1, ids, name, args, context)
        act_amount = self._act(cr, 1, ids, name, args, context)
        for line in self.browse(cr, 1, ids, context=None):
            res[line.id] = {}
            res[line.id]['practical_amount'] = prac_amount[line.id]
            res[line.id]['reserved_amount'] = prac_amount[line.id] - act_amount[line.id]
            res[line.id]['remaining_amount'] = res[line.id]['reserved_amount'] - line.planned_amount
        return res
    
    _columns = {
        'planned_amount':fields.float('Planned Amount', required=True, digits_compute=dp.get_precision('Account'),
                                      help='Please mind the budget amount sign, (-) for expenses, (+) for revenue'),
        'practical_amount':fields.function(_compute_amount, string='Practical Amount', type='float', digits_compute=dp.get_precision('Account'), multi='budget'),
        'reserved_amount': fields.function(_compute_amount, string='Reserved Amount', type='float', digits_compute=dp.get_precision('Account'), readonly=True, multi='budget'),
        'remaining_amount': fields.function(_compute_amount, string='Remaining Amount', type='float', digits_compute=dp.get_precision('Account'), readonly=True, multi='budget'),
        'state_related' : fields.related('crossovered_budget_id', 'state', type="char", string="Budget State"),
        'state' : fields.selection([('draft', 'Draft'), ('cancel', 'Cancelled'), ('confirm', 'Confirmed'), ('validate', 'Validated'), ('done', 'Done')], 'State', select=True, required=True, readonly=True),
    }

    _defaults = {
        'state': 'draft',
    }
    
    def _find_budget_line(self, cr, uid, analytic, account, date):
        account_obj = self.pool.get('account.account')
        analytic_obj = self.pool.get('account.analytic.account')
        dom = [('state', '=', 'validate'), ('crossovered_budget_id.state', '=', 'validate')]
        dom.append(('date_to', '>=', date))
        dom.append(('date_from', '<=', date))
        budget_line_ids = self.search(cr, uid, dom)
        for budget_line in self.browse(cr, uid, budget_line_ids):
            acc_ids = [x.id for x in budget_line.general_budget_id.account_ids]
            acc_ids = account_obj._get_children_and_consol(cr, uid, acc_ids)
#             an_acc_ids = analytic_obj.search(cr, uid, [('parent_id', 'child_of', [budget_line.analytic_account_id.id])])
            an_acc_ids = analytic_obj.search(cr, uid, [('id', '=', budget_line.analytic_account_id.id),('type','!=','view')])
            # old
            if analytic in an_acc_ids and account in acc_ids:
                return budget_line
        return False
    
    def find_budget_line(self, cr, uid, analytic, account, date):
        line = self._find_budget_line(cr, uid, analytic, account, date)
        return line and line.id

    def check_available(self, cr, uid, ids, amount=0.0, context=None):
        for budget_line in self.browse(cr, 1, ids, context):
            if amount > budget_line.remaining_amount :
                raise osv.except_osv(_('Warning!'), _("Insufficient available budget!"))
    
    def assign_budget_line(self, cr, uid, analytic, account, date, obj):
        budget_line = self._find_budget_line(cr, uid, analytic, account, date)
        if not budget_line:
            raise osv.except_osv(_('Warning!'), _("Cannot find allocated budget!"))
        obj.budget_line_id = budget_line.id
            
    def unlink(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids):
            if line.state in ('validate', 'done') and line.crossovered_budget_id.state in ('validate', 'done'):
                raise osv.except_osv(_('Warning !'), _('Unable to delete running budget'))
        return super(crossovered_budget_lines, self).unlink(cr, uid, ids, context)
    
    def create(self, cr, uid, vals, context=None):
        line_id = super(crossovered_budget_lines, self).create(cr, uid, vals, context)
        self.check_overlap(cr, uid, line_id, context)
        return line_id
    
    def write(self, cr, uid, ids, vals, context=None):
        super(crossovered_budget_lines, self).write(cr, uid, ids, vals, context)
        self.check_overlap(cr, uid, ids, context)
        return ids
    
    def check_overlap(self, cr, uid, ids, context=None):
        analytic_obj = self.pool.get('account.analytic.account')
        def overlap():
            raise osv.except_osv(_('Warning !'), _('Budget Line has overlap account!'))
        
        def check_account():
            account_ids2 = line2.general_budget_id.account_ids._get_children_and_consol()
            for account_id in account_ids2:
                if account_id in account_ids:
                    return True
            return False
        
        def check_analytic():
            analytic_ids2 = analytic_obj.search(cr, uid, [('parent_id', 'child_of', [line2.analytic_account_id.id])])
            for analytic_id in analytic_ids2:
                if analytic_id in analytic_ids:
                    return True
            return False
        
        for line in self.browse(cr, uid, ids):
            date_fr = line.date_from
            date_to = line.date_to
            analytic_ids = analytic_obj.search(cr, uid, [('parent_id', 'child_of', [line.analytic_account_id.id])])
            account_ids = line.general_budget_id.account_ids._get_children_and_consol()
            ids2 = self.search(cr, uid, [('state', '!=', 'cancel'),
                                         ('date_to', '>=', date_to),
                                         ('date_from', '<=', date_fr)])
            for line2 in self.browse(cr, uid, ids2):
                if line2.id == line.id:
                    continue
                same_analytic = line2.analytic_account_id.id == line.analytic_account_id.id
                same_post = line2.general_budget_id.id == line.general_budget_id.id
                if same_analytic and same_post:
                    overlap()
                elif same_analytic and not same_post and check_account():
                    overlap()
#                 elif not same_analytic and same_post and check_analytic():
#                     overlap()
#                 elif check_analytic() and check_account():
#                     overlap()
        return True
    
    def button_confirm(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids):
            if line.crossovered_budget_id.state in ['validate', 'done', 'cancel']:
                raise osv.except_osv(_('Warning !'), _('Unable to Confirm Budget Lines in Running Budget \n You have to switch budget!'))
        return self.write(cr, uid, ids, {'state': 'confirm'})
        
    def button_validate(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids):
            if line.crossovered_budget_id.state in ['validate', 'done', 'cancel']:
                raise osv.except_osv(_('Warning !'), _('Unable to Approve Budget Lines in Running Budget \n You have to switch budget!'))
        return self.write(cr, uid, ids, {'state': 'validate'})
    
    def button_cancel(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids):
            if line.reserved_amount != 0 :
                raise osv.except_osv(_('Warning !'), _('Unable to Cancel reserved Budget'))
        return self.write(cr, uid, ids, {'state': 'cancel'})
    
    def button_done(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids):
            if line.state == 'cancel':
                ids.remove(line.id)
        return self.write(cr, uid, ids, {'state': 'done'})
    
    def button_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'draft'})
