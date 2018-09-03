from openerp.osv import fields, osv
from openerp.tools.translate import _
    
class po_line_pr(osv.osv):
    _inherit = 'purchase.order.line'
    
    _columns = {
        'pr_line_id': fields.many2one('stock.purchase.requisition.line', 'PR', copy=False),
    }
    
    def create(self, cr, uid, vals, context=None):
        line_id = super(po_line_pr, self).create(cr, uid, vals, context)
        for order_line in self.browse(cr, uid, line_id):
            if order_line.pr_line_id:
                message = 'Purchase Order %s for %s created' % (order_line.order_id.name, order_line.name)
                order_line.pr_line_id.stock_pr_id.message_post(message)
                order_line.pr_line_id.action_done()
        return line_id
    
class po_pr(osv.osv):
    _inherit = 'purchase.order'
    
    def action_picking_create(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids):
            picking_vals = {
                'picking_type_id': order.picking_type_id.id,
                'partner_id': order.partner_id.id,
                'date': order.date_order,
                'origin': order.name
            }
            if order.origin:
                picking_vals['origin'] += ':' + order.origin
            picking_id = self.pool.get('stock.picking').create(cr, uid, picking_vals, context=context)
            self._create_stock_moves(cr, uid, order, order.order_line, picking_id, context=context)
        return picking_id
    
    def wkf_action_cancel(self, cr, uid, ids, context=None):
        super(po_pr, self).wkf_action_cancel(cr, uid, ids, context)
        for order in self.browse(cr, uid, ids):
            for order_line in order.order_line:
                if order_line.pr_line_id:
                    done = False
                    message = 'Purchase Order %s for %s cancelled' % (order.name, order_line.name)
                    order_line.pr_line_id.stock_pr_id.message_post(message)
                    for line in order_line.pr_line_id.po_line_ids:
                        if line.state == 'done':
                            done = True
                        elif line.state != 'cancel':
                            return True
                    if done:
                        line.pr_line_id.action_done()
                    else :
                        line.pr_line_id.action_cancel()
    
class calls_pr(osv.osv):
    _inherit = 'purchase.requisition'
    
    def _prepare_purchase_order(self, cr, uid, requisition, supplier, context=None):
        vals = super(calls_pr, self)._prepare_purchase_order(cr, uid, requisition, supplier, context)
        if requisition.origin :
            vals['origin'] += ':' + requisition.origin
        return vals
    
    def _prepare_purchase_order_line(self, cr, uid, requisition, requisition_line, purchase_id, supplier, context=None):
        vals = super(calls_pr, self)._prepare_purchase_order_line(cr, uid, requisition, requisition_line, purchase_id, supplier, context)
        vals['name'] = requisition_line.description
        if requisition_line.pr_line_id:
            vals['pr_line_id'] = requisition_line.pr_line_id.id
            vals['price_unit'] = requisition_line.pr_line_id.unit_price
            number = self.pool.get('purchase.order').browse(cr, uid, purchase_id).name
            requisition_line.pr_line_id.stock_pr_id.message_post('Purchase Order %s Created for %s' % (number, requisition_line.pr_line_id.description))
        return vals
    
    def tender_cancel(self, cr, uid, ids, context=None):
        super(calls_pr, self).tender_cancel(cr, uid, ids, context)
        for bids in self.browse(cr, uid, ids):
            for bids_line in bids.line_ids:
                if bids_line.pr_line_id:
                    done = False
                    bids_line.pr_line_id.stock_pr_id.message_post('Calls for Bids %s for %s cancelled' % (bids.name, bids_line.description))
                    for line in bids_line.pr_line_id.bid_line_ids:
                        if line.requisition_id.state == 'done':
                            done = True
                        elif line.requisition_id.state != 'cancel':
                            return True
                    if done:
                        line.pr_line_id.action_done()
                    else :
                        line.pr_line_id.action_cancel()
                        
class calls_line_pr(osv.osv):
    _inherit = 'purchase.requisition.line'
    
    _columns = {
        'pr_line_id': fields.many2one('stock.purchase.requisition.line', 'PR'),
        'description': fields.char('Description'),
    }
    
    def onchange_product_id(self, cr, uid, ids, product_id, product_uom_id, parent_analytic_account, analytic_account, parent_date, date, context=None):
        res = super(calls_line_pr, self).onchange_product_id(cr, uid, ids, product_id, product_uom_id, parent_analytic_account, analytic_account, parent_date, date, context)
        if product_id:
            desc = self.pool.get('product.product').browse(cr,uid,product_id).name
            def_code = self.pool.get('product.product').browse(cr,uid,product_id).default_code
            res['value']['description']="["+def_code+"]"+" "+desc
        return res
    
class procurement_order(osv.osv):
    _inherit = 'procurement.order'

    def _run(self, cr, uid, procurement, context=None):
        requisition_obj = self.pool.get('purchase.requisition')
        warehouse_obj = self.pool.get('stock.warehouse')
        if procurement.rule_id and procurement.rule_id.action == 'buy' and procurement.product_id.purchase_requisition:
            warehouse_id = warehouse_obj.search(cr, uid, [('company_id', '=', procurement.company_id.id)], context=context)
            
            # Kalo di stock move ada analytic account
            if procurement.move_dest_id and procurement.move_dest_id.analytic_account_id:
                analytic = procurement.move_dest_id.analytic_account_id.id
            else:
                analytic = False
                
            requisition_id = requisition_obj.create(cr, uid, {
                'origin': procurement.origin,
                'date_end': procurement.date_planned,
                'warehouse_id': warehouse_id and warehouse_id[0] or False,
                'company_id': procurement.company_id.id,
                'procurement_id': procurement.id,
                'picking_type_id': procurement.rule_id.picking_type_id.id,
                # Add analytic account
                'account_analytic_id': analytic,
                'line_ids': [(0, 0, {
                    'product_id': procurement.product_id.id,
                    'product_uom_id': procurement.product_uom.id,
                    'product_qty': procurement.product_qty,
                    'product_qty': procurement.product_qty,
                    # Add analytic account
                    'account_analytic_id': analytic
                })],
            })
            self.message_post(cr, uid, [procurement.id], body=_("Purchase Requisition created"), context=context)
            return self.write(cr, uid, [procurement.id], {'requisition_id': requisition_id}, context=context)
        return super(procurement_order, self)._run(cr, uid, procurement, context=context)
 
