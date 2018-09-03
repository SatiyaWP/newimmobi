from openerp.osv import fields, osv
from openerp.tools.translate import _


class stock_picking(osv.osv):
    
    _inherit = 'stock.picking'    
    
    _columns = { 
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account'),
    }
    
class stock_move(osv.osv):
    
    _inherit = 'stock.move'
    
    _columns = { 
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account'),
    }
        
class account_move_stock(osv.osv):
    
    _inherit = 'account.move'    
        
    _columns = { 
        'stock_move_id': fields.many2one('stock.move', 'Stock Move', select=True),
    }
        
class stock_quant_analytic(osv.osv):
    
    _inherit = 'stock.quant'    
               
    def _create_account_move_line(self, cr, uid, quants, move, credit_account_id, debit_account_id, journal_id, context=None):
        # group quants by cost
        quant_cost_qty = {}
        for quant in quants:
            if quant_cost_qty.get(quant.cost):
                quant_cost_qty[quant.cost] += quant.qty
            else:
                quant_cost_qty[quant.cost] = quant.qty
        move_obj = self.pool.get('account.move')
        for cost, qty in quant_cost_qty.items():
            move_lines = self._prepare_account_move_line(cr, uid, move, qty, cost, credit_account_id, debit_account_id, context=context)
            period_id = context.get('force_period', self.pool.get('account.period').find(cr, uid, context=context)[0])
            ref = move.picking_id and move.picking_id.name or \
                    (move.raw_material_production_id and move.raw_material_production_id.name) or ''
            move_obj.create(cr, uid, {'journal_id': journal_id,
                                      'line_id': move_lines,
                                      
                                      # Stock Move ID
                                      'stock_move_id': move.id,
                                      
                                      'period_id': period_id,
                                      'date': fields.date.context_today(self, cr, uid, context=context),
                                      'ref': ref}, context=context)
