from datetime import date
import time
from openerp import api
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import except_orm
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class stock_purchase_requisition(osv.osv):
    _name = 'stock.purchase.requisition'    
    _description = 'Purchase Requisition'    
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    def _amount_total(self, cr, uid, ids, f_name, arg, context=None):
        res = {}
        for stock_pr_id in self.browse(cr, uid, ids, context=context):
            res[stock_pr_id.id] = 0
            for stock_pr_line in stock_pr_id.stock_pr_line:
                res[stock_pr_id.id] += stock_pr_line.unit_price
        return res
    
    def _default_users(self, cr, uid, context=None):
        return uid
    
    def _count_all(self, cr, uid, ids, field_name, arg, context=None):
        for pr in self.browse(cr, uid, ids, context=context):
            res = {}
            res[pr.id] = len(pr.picking_ids)
            return res
    
    def _count_po_all(self, cr, uid, ids, field_name, arg, context=None):
        for pr in self.browse(cr, uid, ids, context=context):
            res = {}
            res[pr.id] = len(pr.po_ids)
            return res
        
    def _count_calls_all(self, cr, uid, ids, field_name, arg, context=None):
        for pr in self.browse(cr, uid, ids, context=context):
            res = {}
            res[pr.id] = len(pr.calls_ids)
            return res
    
    def _get_picking_ids(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for pr_id in ids:
            res[pr_id] = []
        query = """
        SELECT picking_id, pr.id FROM stock_picking p, stock_move m, stock_purchase_requisition_line prl, stock_purchase_requisition pr
            WHERE pr.id in %s and pr.id = prl.stock_pr_id and prl.id = m.pr_line_id and m.picking_id = p.id
            GROUP BY picking_id, pr.id
             
        """
        cr.execute(query, (tuple(ids),))
        picks = cr.fetchall()
        for pick_id, pr_id in picks:
            res[pr_id].append(pick_id)
        return res
    
    def _get_po_ids(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for pr_id in ids:
            res[pr_id] = []
        query = """
        SELECT order_id, pr.id FROM purchase_order p, purchase_order_line m, stock_purchase_requisition_line prl, stock_purchase_requisition pr
            WHERE pr.id in %s and pr.id = prl.stock_pr_id and prl.id = m.pr_line_id and m.order_id = p.id
            GROUP BY order_id, pr.id
             
        """
        cr.execute(query, (tuple(ids),))
        orders = cr.fetchall()
        for order_id, pr_id in orders:
            res[pr_id].append(order_id)
        return res
    
    def _get_calls_ids(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for pr_id in ids:
            res[pr_id] = []
        query = """
        SELECT requisition_id, pr.id FROM purchase_requisition p, purchase_requisition_line m, stock_purchase_requisition_line prl, stock_purchase_requisition pr
            WHERE pr.id in %s and pr.id = prl.stock_pr_id and prl.id = m.pr_line_id and m.requisition_id = p.id
            GROUP BY requisition_id, pr.id
              
        """
        cr.execute(query, (tuple(ids),))
        requisition = cr.fetchall()
        for requisition_id, pr_id in requisition:
            res[pr_id].append(requisition_id)
        return res
    
    def _get_warehouse(self, cr, uid, context=None):
        if context is None:
            context = {}
        res = self.pool.get('stock.warehouse').search(cr, uid, [], limit=1)
        return res and res[0] or False
    
    _columns = {
        'name': fields.char('Name', select=True),
        'user_id': fields.many2one('res.users', 'User', required=True, readonly=True),
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'warehouse_id': fields.many2one('stock.warehouse', 'Warehouse', required=True, readonly=True, states={'draft': [('readonly', False)]},),
        'order_date': fields.datetime('Order Date', required=True, readonly=True),
        'schedule_date': fields.datetime('Schedule Date', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'stock_pr_line': fields.one2many('stock.purchase.requisition.line', 'stock_pr_id', 'Requisition Line', copy=True, readonly=True, states={'draft': [('readonly', False)]}),
        'picking_ids': fields.function(_get_picking_ids, method=True, type='one2many', relation='stock.picking', string='Picking List', help="This is the list of receipts that have been generated for this PR order."),
        'po_ids': fields.function(_get_po_ids, method=True, type='one2many', relation='purchase.order', string='PO List', help="This is the list of PO that have been generated for this PR order."),
        'calls_ids': fields.function(_get_calls_ids, method=True, type='one2many', relation='purchase.requisition', string='Calls for Bids List', help="This is the list of Calls for Bids that have been generated for this PR order."),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('cancel', 'Cancelled'),
            ('wait_approval', 'Waiting Approval'),
            ('on_progress', 'On Progress'),
            ('done', 'Done'),
            ], 'State', track_visibility='onchange', readonly=True, copy=False, select=True),
        'shipment_count': fields.function(_count_all, type='integer', string='Incoming Shipments'),
        'po_count': fields.function(_count_po_all, type='integer', string='Purchase Order'),
        'company_id': fields.many2one('res.company', 'Company', required=True, select=1, states={'on_progress': [('readonly', True)], 'done': [('readonly', True)]}),
    }
    
    _defaults = {
        'state': 'draft',
        'warehouse_id': _get_warehouse,
        'order_date': fields.datetime.now,
        'schedule_date': fields.datetime.now,
        'date': fields.datetime.now,
        'user_id':  lambda obj, cr, uid, context: uid,
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid, 'purchase.order', context=c),
    }
    
    def stock_pr_sequence(self, cr, uid, ids, context=None):
        name = self.pool.get('ir.sequence').get(cr, uid, 'stock.purchase.req')
        self.write(cr, uid, ids, {'name':name})
    
    def unlink(self, cr, uid, ids, context=None):
        # Jika bukan state draft tidak bisa di delete
        for pr in self.browse(cr, uid, ids):
            if pr.state != 'draft':
                raise except_orm(_('Warning!'),
                                 _("Cannot delete PR if state is not in 'Draft'."))
        return super(stock_purchase_requisition, self).unlink(cr, uid, ids, context)
    
    def create(self, cr, uid, vals, context=None):
        # Buat Nama PR dengan sequence
        pr_id = super(stock_purchase_requisition, self).create(cr, uid, vals, context)
        self.stock_pr_sequence(cr, uid, [pr_id], context)
        
        # Cek apakah line kosong
        if not vals['stock_pr_line']:
            raise except_orm(_('Warning!'),
                             _('PR line cannot be empty.'))
        return pr_id
    
    def action_set_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state' : 'draft'})
    
    def action_cancel(self, cr, uid, ids, context=None):
        for pr in self.browse(cr, uid, ids):
            for line in pr.stock_pr_line:
                if (not line.bid_line_ids and not line.move_ids) or pr.state != 'on_progress':
                    line.action_cancel()
            for picking in pr.picking_ids:
                if picking.state in ('assigned', 'confirmed', 'partially_available'):
                    picking.action_cancel()
                    picking.message_post('Cancelled by the Request associated to this picking')
            for bids in pr.calls_ids:
                bids.tender_cancel()
                bids.message_post('Cancelled by the Request associated to this picking')
                    
                
                
    def _get_procure_method(self, cr, uid, product, location_id=False, location_dest_id=False, context=None):
        '''This method returns the procure_method to use when creating the stock move for the production raw materials
        Besides the standard configuration of looking if the product or product category has the MTO route,
        you can also define a rule e.g. from Stock to Production (which might be used in the future like the sale orders)
        '''
        warehouse_obj = self.pool['stock.warehouse']
        routes = product.route_ids + product.categ_id.total_route_ids
        if location_id and location_dest_id:
            pull_obj = self.pool['procurement.rule']
            pulls = pull_obj.search(cr, uid, [('route_id', 'in', [x.id for x in routes]),
                                            ('location_id', '=', location_dest_id),
                                            ('location_src_id', '=', location_id)], limit=1, context=context)
            if pulls:
                return pull_obj.browse(cr, uid, pulls[0], context=context).procure_method
        try:
            mto_route = warehouse_obj._get_mto_route(cr, uid, context=context)
        except:
            return "make_to_stock"
        if mto_route in [x.id for x in routes]:
            return "make_to_order"
        return "make_to_stock"
                
    def action_confirm(self, cr, uid, ids, context=None):
        # Cek Reserved Budget
        for pr in self.browse(cr, uid, ids):
            pr.order_date = time.strftime('%Y-%m-%d')
            pr.state = 'wait_approval'
            for line in pr.stock_pr_line:
#                 if not line.product_id.categ_id.asset_categ_id:
                self.pool.get('crossovered.budget.lines').assign_budget_line(cr, uid, line.analytic_account_id.id, line.get_account(), line.get_date(), line)
                price = line.product_id.valuation == 'real_time' and line.standard_price * line.qty or line.subtotal
                line.budget_line_id.check_available(price)
                
    def action_approve(self, cr, uid, ids, context=None):
        pr = self.browse(cr, uid, ids[0])
        stock_picking_obj = self.pool.get('stock.picking')
        stock_move_obj = self.pool.get('stock.move')
        
        # Cek Account Manager
        if uid != pr.analytic_account_id.manager_id.id:
            raise except_orm(_('Warning!'),
                             _('You are not responsible person to approve this PR.'))
            
        for line in pr.stock_pr_line:
            # Change state PR line
            line.state = 'approved'
#             if not line.product_id.categ_id.asset_categ_id:
            self.pool.get('crossovered.budget.lines').assign_budget_line(cr, uid, line.analytic_account_id.id, line.get_account(), line.get_date(), line)
            
        picking_type = line.warehouse_id.int_type_id
        if not picking_type:
            raise osv.except_osv(_('Warning !'), _('No Internal Picking Type configured for warehouse %s') % line.warehouse_id.name)
        if picking_type and not picking_type.default_location_src_id.id:
            raise except_orm(_('Warning!'),
                             _('The source and destination location of Operation Type cannot be empty.'))
        picking_id = False
        desc = ''
        for stock_pr_line in pr.stock_pr_line: 
            # Jika stockable dan bukan merupakan asset
            if stock_pr_line.product_id.type in ('product'):
                if not picking_id: 
                    picking_id = stock_picking_obj.create(cr, uid, {'date': pr.order_date,
                                                                    'min_date': pr.schedule_date,
                                                                    'origin': pr.name,
                                                                    'move_type': 'direct',
                                                                    'picking_type_id': picking_type.id,
                                                                    'priority': '1'})

                procurement = self._get_procure_method(cr, uid, stock_pr_line.product_id,
                                                       picking_type.default_location_src_id.id,
                                                       picking_type.default_location_dest_id.id, context)
                
                stock_move_obj.create(cr, uid, {'picking_id': picking_id,
                                                'product_id': stock_pr_line.product_id.id,
                                                'product_uom_qty': stock_pr_line.qty,
                                                'product_uom': stock_pr_line.uom_id.id,
                                                'name': stock_pr_line.description,
                                                'origin': pr.name,
                                                'picking_type_id': picking_type.id,
                                                'date': pr.order_date,
                                                'date_expected': pr.schedule_date,
                                                'location_id': picking_type.default_location_src_id.id,
                                                'location_dest_id': picking_type.default_location_dest_id.id,
                                                'procure_method': procurement,
                                                'pr_line_id': stock_pr_line.id,
                                                'analytic_account_id': pr.analytic_account_id.id})
                desc += line.product_id.default_code + ', '
        
        # Mark Operation as To Do
        self.write(cr, uid, ids, {'state':'on_progress'})
        
        if picking_id:
            stock_picking_obj.action_confirm(cr, uid, [picking_id], context)
            number = stock_picking_obj.browse(cr, uid, picking_id).name
            pr.message_post('Picking %s Created for %s' % (number, desc[:-2]))
        
    def view_picking(self, cr, uid, ids, context=None):
        '''
        This function returns an action that display existing picking orders of given purchase order ids.
        '''
        if context is None:
            context = {}
        mod_obj = self.pool.get('ir.model.data')
        dummy, action_id = tuple(mod_obj.get_object_reference(cr, uid, 'stock', 'action_picking_tree'))
        action = self.pool.get('ir.actions.act_window').read(cr, uid, action_id, context=context)

        pick_ids = []
        for pr in self.browse(cr, uid, ids, context=context):
            pick_ids += [picking.id for picking in pr.picking_ids]
        
        # override the context to get rid of the default filtering on picking type
        action['context'] = {}
        # choose the view_mode accordingly
        if len(pick_ids) > 1:
            action['domain'] = "[('id','in',[" + ','.join(map(str, pick_ids)) + "])]"
        else:
            res = mod_obj.get_object_reference(cr, uid, 'stock', 'view_picking_form')
            action['views'] = [(res and res[1] or False, 'form')]
            action['res_id'] = pick_ids and pick_ids[0] or False
        return action
        
    def view_po(self, cr, uid, ids, context=None):
        '''
        This function returns an action that display existing purchase orders of given PR order ids.
        '''
        if context is None:
            context = {}
        mod_obj = self.pool.get('ir.model.data')
        dummy, action_id = tuple(mod_obj.get_object_reference(cr, uid, 'purchase', 'purchase_form_action'))
        action = self.pool.get('ir.actions.act_window').read(cr, uid, action_id, context=context)

        po_ids = []
        for pr in self.browse(cr, uid, ids, context=context):
            po_ids += [po.id for po in pr.po_ids]
        
        # override the context to get rid of the default filtering on picking type
        action['context'] = {}
        # choose the view_mode accordingly
        if len(po_ids) > 1:
            action['domain'] = "[('id','in',[" + ','.join(map(str, po_ids)) + "])]"
        else:
            res = mod_obj.get_object_reference(cr, uid, 'purchase', 'purchase_order_form')
            action['views'] = [(res and res[1] or False, 'form')]
            action['res_id'] = po_ids and po_ids[0] or False
        return action
    
class stock_purchase_requisition_line(osv.osv):
    _name = 'stock.purchase.requisition.line'
    
    def _amount_line(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.unit_price * line.qty
        return res
    
    def _res_amt(self, cr, uid, ids, name, args, context=None):
        res = {}
        ress = {}
        result = []
        domain = ""
        for req_line in self.browse(cr, uid, ids):
            ress[req_line.id] = [x.picking_id.name for x in req_line.move_ids]
            if ress[req_line.id]:
                domain += _("(account_id=%s AND general_account_id=%s AND name in (") % (req_line.analytic_account_id.id, req_line.get_account())
                sub_domain = ""
                for name in ress[req_line.id]:
                    sub_domain += _("'%s',") % name
                domain += sub_domain[:-1] + ")) or "
        if domain:
            cr.execute("SELECT name, SUM(amount) FROM account_analytic_line WHERE %s GROUP BY name" % domain[:-4])
            result = cr.fetchall()
        for line_id in ress:
            res[line_id] = (req_line.standard_price * req_line.qty)
            for name in ress[line_id]:
                for an_name in result:
                    if an_name == name:
                        res[req_line.id] += result[an_name]
        return res
    
    _columns = {
        'product_id': fields.many2one('product.product', 'Product', required=True),
        'stock_pr_id': fields.many2one('stock.purchase.requisition', 'Reference'),
        'budget_line_id': fields.many2one('crossovered.budget.lines', 'Budget Line', select=True),
        'move_ids': fields.one2many('stock.move', 'pr_line_id', 'Reservation', readonly=True, ondelete='set null'),
        'bid_line_ids': fields.one2many('purchase.requisition.line', 'pr_line_id', 'Reservation', readonly=True, ondelete='set null'),
        'po_line_ids': fields.one2many('purchase.order.line', 'pr_line_id', 'Reservation', readonly=True, ondelete='set null'),
        'description': fields.char('Description', required=True),
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account', required=True),
        'schedule_date': fields.datetime('Schedule Date', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'date': fields.datetime('Processed Date'),
        'qty': fields.float('Quantity', required=True),
        'uom_id': fields.many2one('product.uom', 'Unit of Measure', required=True),
        'unit_price': fields.float('Unit Price', required=True),
        'standard_price': fields.float('Standard Price', required=False),
        'subtotal': fields.function(_amount_line, string='Subtotal', digits_compute=dp.get_precision('Account')),
        'budget_remaining': fields.related('budget_line_id', 'remaining_amount', string="Budget Remaining",
                                           type="float", digits_compute=dp.get_precision('Account'), readonly=True),
        'warehouse_id': fields.related('stock_pr_id', 'warehouse_id', string="Deliver To",
                                           type="many2one", relation='stock.warehouse', readonly=True),
        'user_id': fields.related('stock_pr_id', 'user_id', string="Requestor",
                                           type="many2one", relation='res.users', readonly=True),
        'reserved_amount': fields.function(_res_amt, string='Remaining Reserved Amount', type='float',
                                            digits_compute=dp.get_precision('Account'), readonly=True),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('cancel', 'Cancelled'),
            ('done', 'Done'),
            ('approved', 'Approved')
            ], 'State', readonly=True, copy=False),
    }    
    
    _defaults = {
        'state': 'draft',
    }
    
    def get_account(self, cr, uid, ids, product_id=False, context=None):
        uid = 1
        if product_id :
            product_id = self.pool.get('product.product').browse(cr, uid, product_id)
        else:
            product_id = self.browse(cr, uid, ids[0]).product_id
        categ = product_id.categ_id
#         account = categ.asset_categ_id and categ.asset_categ_id.account_asset_id
#         if account:
#             return account.id
        if product_id.valuation == 'manual_periodic':
            account = product_id.property_account_expense
            while not account and categ:
                account = categ.property_account_expense_categ
                categ = categ.parent_id
        else:
            account = product_id.property_stock_account_output
            while not account and categ:
                account = categ.property_stock_account_output_categ
                categ = categ.parent_id
        if not account:
            raise osv.except_osv(_('Warning !'), _('Expense Account for %s is Empty, \n Go to Product->Accounting->Internal Category') % (product_id.name))
        return account.id
    
    @api.multi
    def get_date(self, stock_pr_id=False):
        if stock_pr_id :
            return self.stock_pr_id.browse(stock_pr_id).order_date[:10]
        for line in self:
            return line.stock_pr_id.order_date[:10]
    
    @api.model
    @api.returns('self', lambda value:value.id)
    def create(self, vals):
        date = self.get_date(vals.get('stock_pr_id', False))
        account = self.get_account(vals.get('product_id', False))
        vals['budget_line_id'] = self.env['crossovered.budget.lines'].find_budget_line(vals['analytic_account_id'], account, date)
        return super(stock_purchase_requisition_line, self).create(vals)
    
    @api.multi
    def write(self, vals):
        for s in self:
            if vals.keys() in ['product_id', 'account_analytic_id'] or not s.budget_line_id:
                date = self.get_date()
                account = s.get_account(vals.get('product_id', False))
                analytic = vals.get('analytic_account_id', False) or s.analytic_account_id.id
                vals['budget_line_id'] = self.env['crossovered.budget.lines'].find_budget_line(analytic, account, date)
        return super(stock_purchase_requisition_line, self).write(vals)
    
    def action_cancel(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids):
            line.state = 'cancel'
            done = False
            for line in line.stock_pr_id.stock_pr_line:
                if line.state == 'done':
                    done = True
                elif line.state != 'cancel':
                    return True
            line.stock_pr_id.state = done and 'done' or 'cancel'
            
    def action_done(self, cr, uid, ids, context=None):
        for line in self.browse(cr, uid, ids):
            line.state = 'done'
            line.date = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            for line in line.stock_pr_id.stock_pr_line:
                if line.state not in ('cancel', 'done'):
                    return True
            line.stock_pr_id.state = 'done'

    def change_product_id(self, cr, uid, ids, product_id, aa_id, sc_date, context=None):
        if not aa_id:
            raise except_orm(_('Warning!'),
                             _('Please fill the Analytic Account field.'))
        if not product_id:
            return {
                'value': {
                    'analytic_account_id': False,
                    'description': False,
                    'qty': 0,
                    'uom_id': False,
                    'unit_price': 0,
                    'schedule_date': False,
                }
            }
        prod = self.pool.get('product.product').browse(cr, uid, product_id)
        if prod.default_code:
            name = '[' + prod.default_code + '] ' + prod.name
        else:
            name = prod.name
        return {
            'value': {
                'analytic_account_id': aa_id,
                'description': name,
                'qty': 1,
                'uom_id': prod.uom_id.id,
                'unit_price': prod.standard_price,
                'standard_price': prod.standard_price,
                'schedule_date': sc_date,
            }
        }
    
class account_analytic_account_user(osv.osv):
    _inherit = 'account.analytic.account'
    
    _columns = {
        'user_ids': fields.many2many('res.users', 'analytic_user_rel', 'user_ids', 'analytic_id', 'Allowed User'),
    }
