from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import SUPERUSER_ID, workflow, api
import openerp.addons.decimal_precision as dp
from datetime import datetime

# class purchase_order(osv.osv):
#     _inherit = 'purchase.order'
    
#     def wkf_confirm_order(self, cr, uid, ids, context=None):
#         cur_obj = self.pool.get('res.currency')
#         acc_obj = self.pool.get('account.account')
#         for order_line in self.browse(cr, uid, ids).order_line:
#             acc_id = order_line.get_account()
#             report_type = acc_obj.browse(cr, uid, acc_id, context=None).user_type.report_type
#             if  report_type not in ['asset', 'liability']:
#                 analytic = order_line.account_analytic_id
#                 self.pool.get('crossovered.budget.lines').assign_budget_line(cr, uid, analytic.id, acc_id, order_line.get_date(), order_line)
#                 company_currency = order_line.order_id.company_id.currency_id.id
#                 price = cur_obj.compute(cr, uid, order_line.order_id.currency_id.id, company_currency, order_line.price_subtotal)
#                 order_line.budget_line_id.check_available(price)
#         super(purchase_order, self).wkf_confirm_order(cr, uid, ids, context)
#         return True
#  
#     def wkf_approve_order(self, cr, uid, ids, context=None):
#         super(purchase_order, self).wkf_approve_order(cr, uid, ids, context)
#         acc_obj = self.pool.get('account.account')
#         for order_line in self.browse(cr, uid, ids).order_line:
#             acc_id = order_line.get_account()
#             report_type = acc_obj.browse(cr, uid, acc_id, context=None).user_type.report_type
#             if  report_type not in ['asset', 'liability']:
#                 analytic = order_line.account_analytic_id
#                 self.pool.get('crossovered.budget.lines').assign_budget_line(cr, uid, analytic.id, acc_id, order_line.get_date(), order_line)
#                 order_line.budget_line_id.check_available()
#         return True
#     
#     def picking_done(self, cr, uid, ids, context=None):
#         super(purchase_order, self).picking_done(cr, uid, ids, context)
#         for po in self.browse(cr, uid, ids, context=context):
#             if all(line.invoiced for line in po.order_line):
#                 po.invoiced = True
#         return True
                
class purchase_order_line(osv.osv):
    _inherit = 'purchase.order.line'

    def _res_amt(self, cr, uid, ids, name, args, context=None):
        if context is None:
            context = {}
        ctx = context.copy()
        res = {}
        com_cur = self.pool.get('res.users').browse(cr, uid, uid, context=None).company_id.currency_id
        
        for order_line in self.browse(cr, uid, ids):
            ord_cur = order_line.order_id.currency_id
            cur_obj = self.pool.get('res.currency')
            result = 0.0
            if order_line.product_id.valuation == 'manual_periodic':
                # cari di order_line.date_invoice
                for invoice_line in order_line.invoice_lines:
                    ctx['date'] = invoice_line.invoice_id.date_invoice
                    # Codingan dulu
                    result -= invoice_line.invoice_id.state != 'draft' and cur_obj.compute(cr, uid, ord_cur.id, com_cur.id, invoice_line.price_subtotal, context=ctx)  or 0.0
                    
            else:
                # cari di move.date
                for move in order_line.move_ids:
                    full_date = datetime.strptime(move.date, '%Y-%m-%d %H:%M:%S')
                    short_date = full_date.strftime('%Y-%m-%d')
                    ctx['date'] = short_date
                    # Codingan dulu
                    result -= move.state == 'done' and cur_obj.compute(cr, uid, ord_cur.id, com_cur.id, (move.purchase_line_id.price_unit * move.product_uom_qty), context=ctx)  or 0.0
            # untuk order_line.order_id.date_order
            full_date = datetime.strptime(order_line.order_id.date_order, '%Y-%m-%d %H:%M:%S')
            short_date = full_date.strftime('%Y-%m-%d')
            ctx['date'] = short_date
            res[order_line.id] = cur_obj.compute(cr, uid, ord_cur.id, com_cur.id, order_line.price_subtotal, context=ctx) + result
            if res[order_line.id] < 0:
                res[order_line.id] = 0
        return res
    
    def _get_coa(self, cr, uid, ids, name, args, context=None):
        res = {}
        for order_line in self.browse(cr, uid, ids):
            prod_id = order_line.product_id.id
            acc_id = order_line.get_account(prod_id)
            res[order_line.id] = acc_id
        return res
    
    def _get_qty_os(self, cr, uid, ids, name, args, context=None):
        res = {}
        for order_line in self.browse(cr, uid, ids):
            produ_rec = order_line.product_id
            prod_qty = order_line.product_qty
            qty_act = 0
            if produ_rec.valuation == 'real_time':
                mv_ids = order_line.move_ids
                for move in mv_ids:
                    if move.state == 'done':
                        qty = move.product_uom_qty
                        qty_act = qty_act + qty
                res[order_line.id] = prod_qty-qty_act
            else:
                inv_line_ids = order_line.invoice_lines
                for inv_l in inv_line_ids:
                    if inv_l.invoice_id.state not in ['draft', 'cancel']:
                        qty = inv_l.quantity
                        qty_act = qty_act + qty
                res[order_line.id] = prod_qty-qty_act
        return res
    
    def _get_amount_os(self, cr, uid, ids, name, args, context=None):
        res = {}
        for order_line in self.browse(cr, uid, ids):
            qty_os = order_line.qty_os
            price = order_line.price_unit            
            res[order_line.id] = qty_os * price
        return res
        
    _columns = {
        'budget_remaining': fields.related('budget_line_id', 'remaining_amount', string="Budget Remaining", type="float", readonly=True),
        'reserved_amount': fields.function(_res_amt, string='Remaining Reserved Amount', type='float', digits_compute=dp.get_precision('Account'), readonly=True),
        'state_po_related': fields.related('order_id', 'state', string="State", type="char"),
        'budget_line_id': fields.many2one('crossovered.budget.lines', 'Budget Lines', readonly=True, select=True),
        'coa_id': fields.function(_get_coa, string="COA Name", type='many2one', relation='account.account'),
        'qty_os': fields.function(_get_qty_os, string="Qty Outstanding", type='float'),
        'amount_os': fields.function(_get_amount_os, string="Amount Outstanding", type='float'),
    }
    
    @api.multi
    def get_account(self, product_id=False):
        if product_id :
            product_id = self.product_id.browse(product_id)
        for line in self:
            product_id = line.product_id
        
        if product_id.valuation == 'manual_periodic':
            account = product_id.property_account_expense or \
                                        product_id.categ_id.property_account_expense_categ
        else:
            account = product_id.categ_id.property_stock_valuation_account_id
        if not account:
            raise osv.except_osv(_('Warning !'), _('Valuation or Expense Account for %s is Empty, \n Go to Product->Accounting->Internal Category') % (product_id.name))
        return account.id
    
    @api.multi
    def get_date(self, order_id=False):
        if order_id :
            return self.order_id.browse(order_id).date_order[:10]
        for line in self:
            return line.order_id.date_order[:10]
        
    @api.model
    @api.returns('self', lambda value:value.id)
    def create(self, vals):
        date = self.get_date(vals.get('order_id', False))
        account = self.get_account(vals.get('product_id', False))
        analytic_account = vals.get('account_analytic_id',False)
        vals['budget_line_id'] = self.env['crossovered.budget.lines'].find_budget_line(analytic_account, account, date)
        return super(purchase_order_line, self).create(vals)
    
    @api.multi
    def write(self, vals):
        for s in self:
            if (vals.keys() in ['product_id', 'account_analytic_id'] or not s.budget_line_id):
                date = s.get_date()
                account = s.get_account(vals.get('product_id', False))
                analytic = vals.get('account_analytic_id', False) or s.account_analytic_id.id
                vals['budget_line_id'] = self.env['crossovered.budget.lines'].find_budget_line(analytic, account, date)
        return super(purchase_order_line, self).write(vals)
    
# class stock_move(osv.osv):
#     _inherit = 'stock.move'
#     
#     def action_cancel(self, cr, uid, ids, context=None):
#         super(stock_move, self).action_cancel(cr, uid, ids, context)
#         line_ids = []
#         for move in self.browse(cr, uid, ids, context):
#             if move.purchase_line_id and (move.purchase_line_id.order_id.invoice_method == 'picking' and \
#                 not self.search(cr, uid, [('purchase_line_id', '=', move.purchase_line_id.id), ('id', '!=', move.id)]) \
#                 or all(line.invoice_id.state not in ['draft', 'cancel'] for line in move.purchase_line_id.invoice_lines)):
#                 line_ids.append(move.purchase_line_id.id)
#         if line_ids:
#             self.pool.get('purchase.order.line').write(cr, uid, line_ids, {'invoiced': True})
            
# class account_invoice(osv.Model):
#     _inherit = 'account.invoice'
# 
#     def invoice_validate(self, cr, uid, ids, context=None):
#         res = super(account_invoice, self).invoice_validate(cr, uid, ids, context=context)
#         purchase_order_obj = self.pool.get('purchase.order')
#         # read access on purchase.order object is not required
#         if not purchase_order_obj.check_access_rights(cr, uid, 'read', raise_exception=False):
#             user_id = SUPERUSER_ID
#         else:
#             user_id = uid
#         po_ids = purchase_order_obj.search(cr, user_id, [('invoice_ids', 'in', ids)], context=context)
#         for order in purchase_order_obj.browse(cr, user_id, po_ids, context=context):
#             invoiced = []
#             shipped = True
#             # for invoice method manual or order, don't care about shipping state
#             # for invoices based on incoming shippment, beware of partial deliveries
#             if (order.invoice_method == 'picking' and
#                     not all(picking.invoice_state in ['invoiced'] for picking in order.picking_ids if picking.state != 'cancel')):
#                 shipped = False
#             for po_line in order.order_line:
#                 if (po_line.invoice_lines and 
#                         all(line.invoice_id.state not in ['draft', 'cancel'] for line in po_line.invoice_lines)):
#                     invoiced.append(po_line.id)
#             if invoiced and shipped:
#                 self.pool['purchase.order.line'].write(cr, user_id, invoiced, {'invoiced': True})
#             workflow.trg_write(user_id, 'purchase.order', order.id, cr)
#         return res
