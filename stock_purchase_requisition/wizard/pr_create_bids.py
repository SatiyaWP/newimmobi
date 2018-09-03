from openerp.osv import osv
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta
from datetime import datetime

class pr_create_bids(osv.osv_memory):
    
    _name = 'pr.create.bids'
    _description = 'Wizard Create Call for Bids from PR'
    
    def create_bids(self, cr, uid, ids, context=None):
        calls_obj = self.pool.get('purchase.requisition')
        calls_lines = []
        pr_ids = []
        schedule_date = False
        lines = self.pool.get('stock.purchase.requisition.line').browse(cr, uid, context.get('active_ids', []))
        if not lines:
            raise osv.except_osv(_('Warning !'), _('You have to choose at least a Line'))
        
        for line in lines:
            # Membuat call for bid line
            calls_lines.append((0, 0, {
                                            'product_id': line.product_id.id,
                                            'description': line.description,
                                            'product_qty': line.qty,
                                            'product_uom_id': line.uom_id.id,
                                            'schedule_date': line.schedule_date,
                                            'account_analytic_id': line.analytic_account_id.id,
                                            'pr_line_id': line.id,
                                            }))
            if line.stock_pr_id not in pr_ids:
                pr_ids.append(line.stock_pr_id)
                
            if not schedule_date or schedule_date > line.schedule_date:
                schedule_date = line.schedule_date
                
        origin = ''
        for pr_id in pr_ids:
            origin += pr_id.name + ','
        
        order_date = (datetime.strptime(schedule_date, '%Y-%m-%d %H:%M:%S') - relativedelta(days=line.stock_pr_id.company_id.po_lead))
        order_date = order_date.strftime('%Y-%m-%d')
        
        if not line.warehouse_id.in_type_id:
            raise osv.except_osv(_('Warning !'), _('No Internal Picking Type configured for warehouse %s') % line.warehouse_id.name)
        
        number = self.pool.get('ir.sequence').get(cr, uid, 'purchase.order.requisition')
        calls_id = calls_obj.create(cr, uid, {    
                                        'name': number,
                                        'origin' : origin[:-1],
                                        'user_id': uid,
                                        'exclusive': 'exclusive',
                                        'date_end': order_date,
                                        'ordering_date': order_date,
                                        'schedule_date': schedule_date,
                                        'picking_type_id': line.warehouse_id.in_type_id.id,
                                        'line_ids' : calls_lines,
                                        })
        
        for line in lines :
            line.stock_pr_id.message_post('Calls for Bids %s Created for %s' % (number, line.description))
            
        return {
            'res_id':calls_id,
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'purchase.requisition',
            'res_model': 'purchase.requisition',
            'type': 'ir.actions.act_window',
        }
            
class purchase_line_invoice(osv.osv_memory):

    _inherit = 'purchase.order.line_invoice'

    def makeInvoices(self, cr, uid, ids, context=None):
        if context is None:
            context={}

        record_ids =  context.get('active_ids',[])
        if record_ids:
            res = False
            invoices = {}
            invoice_obj = self.pool.get('account.invoice')
            purchase_obj = self.pool.get('purchase.order')
            purchase_line_obj = self.pool.get('purchase.order.line')
            invoice_line_obj = self.pool.get('account.invoice.line')
            account_jrnl_obj = self.pool.get('account.journal')

            def multiple_order_invoice_notes(orders):
                notes = ""
                for order in orders:
                    if order.notes:
                        notes += "%s \n" % order.notes
                return notes

            def make_invoice_by_partner(partner, orders, lines_ids):
                """
                    create a new invoice for one supplier
                    @param partner : The object partner
                    @param orders : The set of orders to add in the invoice
                    @param lines : The list of line's id
                """
                origin = ''
                for order in orders:
                    origin += order.name
                    if order.origin:
                        origin += ':' + order.origin
                    origin +=  ', '
                journal_id = account_jrnl_obj.search(cr, uid, [('type', '=', 'purchase')], context=None)
                journal_id = journal_id and journal_id[0] or False
                a = partner.property_account_payable.id
                inv = {
                    'name': origin[:-2],
                    'origin': origin[:-2],
                    'type': 'in_invoice',
                    'journal_id':journal_id,
                    'reference' : partner.ref,
                    'account_id': a,
                    'partner_id': partner.id,
                    'invoice_line': [(6,0,lines_ids)],
                    'currency_id' : orders[0].currency_id.id,
                    'comment': multiple_order_invoice_notes(orders),
                    'payment_term': orders[0].payment_term_id.id,
                    'fiscal_position': partner.property_account_position.id
                }
                inv_id = invoice_obj.create(cr, uid, inv)
                for order in orders:
                    order.write({'invoice_ids': [(4, inv_id)]})
                return inv_id

            for line in purchase_line_obj.browse(cr, uid, record_ids, context=context):
                if (not line.invoiced) and (line.state not in ('draft', 'cancel')):
                    if not line.partner_id.id in invoices:
                        invoices[line.partner_id.id] = []
                    acc_id = purchase_obj._choose_account_from_po_line(cr, uid, line, context=context)
                    inv_line_data = purchase_obj._prepare_inv_line(cr, uid, acc_id, line, context=context)
                    inv_line_data.update({'origin': line.order_id.name})
                    inv_id = invoice_line_obj.create(cr, uid, inv_line_data, context=context)
                    purchase_line_obj.write(cr, uid, [line.id], {'invoiced': True, 'invoice_lines': [(4, inv_id)]})
                    invoices[line.partner_id.id].append((line,inv_id))

            res = []
            for result in invoices.values():
                il = map(lambda x: x[1], result)
                orders = list(set(map(lambda x : x[0].order_id, result)))

                res.append(make_invoice_by_partner(orders[0].partner_id, orders, il))

        return {
            'domain': "[('id','in', ["+','.join(map(str,res))+"])]",
            'name': _('Supplier Invoices'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'view_id': False,
            'context': "{'type':'in_invoice', 'journal_type': 'purchase'}",
            'type': 'ir.actions.act_window'
        }