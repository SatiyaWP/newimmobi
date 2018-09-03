from openerp.osv import fields, osv

class stock_picking(osv.osv):
    _inherit = 'stock.picking'
    
    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        vals = super(stock_picking, self)._get_invoice_vals(cr, uid, key, inv_type, journal_id, move, context)
        if move.picking_id.origin:
            vals['origin'] += ':' + move.picking_id.origin
        return vals
    
class stock_move_pr(osv.osv):
    _inherit = 'stock.move'
    
    _columns = {
        'pr_line_id': fields.many2one('stock.purchase.requisition.line', 'PR'),
        'account_moves': fields.one2many('account.move', 'stock_move_id', 'Account Move', copy=False),
    }
    
    def action_done(self, cr, uid, ids, context=None):
        res = super(stock_move_pr, self).action_done(cr, uid, ids, context)
        for move in self.browse(cr, uid, ids):
            if move.pr_line_id:
                message = '%s %s [%s] %s sent' % (move.product_uom_qty, move.product_uom.name, move.product_id.default_code, move.product_id.name)
                move.pr_line_id.stock_pr_id.message_post(message)
                move.pr_line_id.action_done()
        return res
    
    def action_cancel(self, cr, uid, ids, context=None):
        res = super(stock_move_pr, self).action_cancel(cr, uid, ids, context)
        # Mencari PR id dari salah satu stock move saja
        for move in self.browse(cr, uid, ids):
            if move.pr_line_id:
                done = False
                message = '%s %s [%s] %s ' % (move.product_uom_qty, move.product_uom.name, move.product_id.default_code, move.product_id.name)
                move.pr_line_id.stock_pr_id.message_post('Transfer ' + message + 'cancelled')
                for move in move.pr_line_id.move_ids:
                    if move.state == 'done':
                        done = True
                    elif move.state != 'cancel':
                        return True
                if done:
                    move.pr_line_id.action_done()
                else :
                    move.pr_line_id.action_cancel()
        return res
    
class stock_quant_pr(osv.osv):
    _inherit = 'stock.quant'
    
    def _prepare_account_move_line(self, cr, uid, move, qty, cost, credit_account_id, debit_account_id, context=None):
        debit_line_vals, credit_line_vals = super(stock_quant_pr, self)._prepare_account_move_line(cr, uid, move, qty, cost, credit_account_id, debit_account_id, context)
        # Mencari account pada Capex
        if move.analytic_account_id and move.pr_line_id:
            budget_account = move.pr_line_id.get_account()
            if budget_account == debit_line_vals[2]['account_id']:
                debit_line_vals[2]['analytic_account_id'] = move.analytic_account_id.id
            elif budget_account == credit_line_vals[2]['account_id']:
                credit_line_vals[2]['analytic_account_id'] = move.analytic_account_id.id
        return [debit_line_vals, credit_line_vals]
